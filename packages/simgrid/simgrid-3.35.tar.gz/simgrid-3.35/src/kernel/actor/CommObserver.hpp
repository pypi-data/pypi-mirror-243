/* Copyright (c) 2019-2023. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#ifndef SIMGRID_MC_SIMCALL_COMM_OBSERVER_HPP
#define SIMGRID_MC_SIMCALL_COMM_OBSERVER_HPP

#include "simgrid/forward.h"
#include "src/kernel/actor/SimcallObserver.hpp"
#include "src/mc/transition/Transition.hpp"
#include "xbt/asserts.h"

#include <string>
#include <string_view>

namespace simgrid::kernel::actor {

class ActivityTestSimcall final : public ResultingSimcall<bool> {
  activity::ActivityImpl* const activity_;
  std::string fun_call_;

public:
  ActivityTestSimcall(ActorImpl* actor, activity::ActivityImpl* activity, std::string_view fun_call)
      : ResultingSimcall(actor, true), activity_(activity), fun_call_(fun_call)
  {
  }
  activity::ActivityImpl* get_activity() const { return activity_; }
  void serialize(std::stringstream& stream) const override;
  std::string to_string() const override;
};

class ActivityTestanySimcall final : public ResultingSimcall<ssize_t> {
  const std::vector<activity::ActivityImpl*>& activities_;
  std::vector<int> indexes_; // indexes in activities_ pointing to ready activities (=whose test() is positive)
  int next_value_ = 0;
  std::string fun_call_;

public:
  ActivityTestanySimcall(ActorImpl* actor, const std::vector<activity::ActivityImpl*>& activities,
                         std::string_view fun_call);
  bool is_enabled() override { return true; /* can return -1 if no activity is ready */ }
  void serialize(std::stringstream& stream) const override;
  std::string to_string() const override;
  int get_max_consider() const override;
  void prepare(int times_considered) override;
  const std::vector<activity::ActivityImpl*>& get_activities() const { return activities_; }
  int get_value() const { return next_value_; }
};

class ActivityWaitSimcall final : public ResultingSimcall<bool> {
  activity::ActivityImpl* activity_;
  const double timeout_;
  std::string fun_call_;

public:
  ActivityWaitSimcall(ActorImpl* actor, activity::ActivityImpl* activity, double timeout, std::string_view fun_call)
      : ResultingSimcall(actor, false), activity_(activity), timeout_(timeout), fun_call_(fun_call)
  {
  }
  void serialize(std::stringstream& stream) const override;
  std::string to_string() const override;
  bool is_enabled() override;
  activity::ActivityImpl* get_activity() const { return activity_; }
  void set_activity(activity::ActivityImpl* activity) { activity_ = activity; }
  double get_timeout() const { return timeout_; }
};

class ActivityWaitanySimcall final : public ResultingSimcall<ssize_t> {
  const std::vector<activity::ActivityImpl*>& activities_;
  std::vector<int> indexes_; // indexes in activities_ pointing to ready activities (=whose test() is positive)
  const double timeout_;
  int next_value_ = 0;
  std::string fun_call_;

public:
  ActivityWaitanySimcall(ActorImpl* actor, const std::vector<activity::ActivityImpl*>& activities, double timeout,
                         std::string_view fun_call);
  bool is_enabled() override;
  void serialize(std::stringstream& stream) const override;
  std::string to_string() const override;
  void prepare(int times_considered) override;
  int get_max_consider() const override;
  const std::vector<activity::ActivityImpl*>& get_activities() const { return activities_; }
  double get_timeout() const { return timeout_; }
  int get_value() const { return next_value_; }
};

class CommIsendSimcall final : public SimcallObserver {
  activity::MailboxImpl* mbox_;
  double payload_size_;
  double rate_;
  unsigned char* src_buff_;
  size_t src_buff_size_;
  void* payload_;
  bool detached_;
  activity::CommImpl* comm_ = {};
  int tag_                  = {};

  std::function<bool(void*, void*, activity::CommImpl*)> match_fun_;
  std::function<void(void*)> clean_fun_; // used to free the synchro in case of problem after a detached send
  std::function<void(activity::CommImpl*, void*, size_t)> copy_data_fun_; // used to copy data if not default one

  std::string fun_call_;

public:
  CommIsendSimcall(
      ActorImpl* actor, activity::MailboxImpl* mbox, double payload_size, double rate, unsigned char* src_buff,
      size_t src_buff_size, const std::function<bool(void*, void*, activity::CommImpl*)>& match_fun,
      const std::function<void(void*)>& clean_fun, // used to free the synchro in case of problem after a detached send
      const std::function<void(activity::CommImpl*, void*, size_t)>&
          copy_data_fun, // used to copy data if not default one
      void* payload, bool detached, std::string_view fun_call)
      : SimcallObserver(actor)
      , mbox_(mbox)
      , payload_size_(payload_size)
      , rate_(rate)
      , src_buff_(src_buff)
      , src_buff_size_(src_buff_size)
      , payload_(payload)
      , detached_(detached)
      , match_fun_(match_fun)
      , clean_fun_(clean_fun)
      , copy_data_fun_(copy_data_fun)
      , fun_call_(fun_call)
  {
  }
  void serialize(std::stringstream& stream) const override;
  std::string to_string() const override;
  activity::MailboxImpl* get_mailbox() const { return mbox_; }
  double get_payload_size() const { return payload_size_; }
  double get_rate() const { return rate_; }
  unsigned char* get_src_buff() const { return src_buff_; }
  size_t get_src_buff_size() const { return src_buff_size_; }
  void* get_payload() const { return payload_; }
  bool is_detached() const { return detached_; }
  void set_comm(activity::CommImpl* comm) { comm_ = comm; }
  void set_tag(int tag) { tag_ = tag; }

  auto const& get_match_fun() const { return match_fun_; }
  auto const& get_clean_fun() const { return clean_fun_; }
  auto const& get_copy_data_fun() const { return copy_data_fun_; }
};

class CommIrecvSimcall final : public SimcallObserver {
  activity::MailboxImpl* mbox_;
  unsigned char* dst_buff_;
  size_t* dst_buff_size_;
  void* payload_;
  double rate_;
  activity::CommImpl* comm_ = {};
  int tag_                  = {};

  std::function<bool(void*, void*, activity::CommImpl*)> match_fun_;
  std::function<void(activity::CommImpl*, void*, size_t)> copy_data_fun_; // used to copy data if not default one

  std::string fun_call_;

public:
  CommIrecvSimcall(ActorImpl* actor, activity::MailboxImpl* mbox, unsigned char* dst_buff, size_t* dst_buff_size,
                   const std::function<bool(void*, void*, activity::CommImpl*)>& match_fun,
                   const std::function<void(activity::CommImpl*, void*, size_t)>& copy_data_fun, void* payload,
                   double rate, std::string_view fun_call)
      : SimcallObserver(actor)
      , mbox_(mbox)
      , dst_buff_(dst_buff)
      , dst_buff_size_(dst_buff_size)
      , payload_(payload)
      , rate_(rate)
      , match_fun_(match_fun)
      , copy_data_fun_(copy_data_fun)
      , fun_call_(fun_call)
  {
  }
  void serialize(std::stringstream& stream) const override;
  std::string to_string() const override;
  activity::MailboxImpl* get_mailbox() const { return mbox_; }
  double get_rate() const { return rate_; }
  unsigned char* get_dst_buff() const { return dst_buff_; }
  size_t* get_dst_buff_size() const { return dst_buff_size_; }
  void* get_payload() const { return payload_; }
  void set_comm(activity::CommImpl* comm) { comm_ = comm; }
  void set_tag(int tag) { tag_ = tag; }

  auto const& get_match_fun() const { return match_fun_; };
  auto const& get_copy_data_fun() const { return copy_data_fun_; }
};

class MessIputSimcall final : public SimcallObserver {
  activity::MessageQueueImpl* queue_;
  void* payload_;
  activity::MessImpl* mess_ = {};

public:
  MessIputSimcall(
      ActorImpl* actor, activity::MessageQueueImpl* queue, void* payload)
      : SimcallObserver(actor)
      , queue_(queue)
      , payload_(payload)
  {
  }
  void serialize(std::stringstream& stream) const override;
  std::string to_string() const override;
  activity::MessageQueueImpl* get_queue() const { return queue_; }
  void* get_payload() const { return payload_; }
  void set_message(activity::MessImpl* mess) { mess_ = mess; }
};

class MessIgetSimcall final : public SimcallObserver {
  activity::MessageQueueImpl* queue_;
  unsigned char* dst_buff_;
  size_t* dst_buff_size_;
  void* payload_;
  activity::MessImpl* mess_ = {};

public:
  MessIgetSimcall(ActorImpl* actor, activity::MessageQueueImpl* queue, unsigned char* dst_buff, size_t* dst_buff_size,
                  void* payload)
      : SimcallObserver(actor)
      , queue_(queue)
      , dst_buff_(dst_buff)
      , dst_buff_size_(dst_buff_size)
      , payload_(payload)
  {
  }
  void serialize(std::stringstream& stream) const override;
  std::string to_string() const override;
  activity::MessageQueueImpl* get_queue() const { return queue_; }
  unsigned char* get_dst_buff() const { return dst_buff_; }
  size_t* get_dst_buff_size() const { return dst_buff_size_; }
  void* get_payload() const { return payload_; }
  void set_message(activity::MessImpl* mess) { mess_ = mess; }
};

} // namespace simgrid::kernel::actor

#endif
