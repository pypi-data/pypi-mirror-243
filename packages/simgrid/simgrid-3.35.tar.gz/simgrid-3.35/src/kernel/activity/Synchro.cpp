/* Copyright (c) 2007-2023. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include <simgrid/Exception.hpp>
#include <simgrid/s4u/Host.hpp>

#include "src/kernel/activity/Synchro.hpp"
#include "src/kernel/actor/ActorImpl.hpp"
#include "src/kernel/resource/CpuImpl.hpp"

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(ker_synchro, kernel,
                                "Kernel synchronization activity (lock/acquire on a mutex, semaphore or condition)");

namespace simgrid::kernel::activity {

SynchroImpl& SynchroImpl::set_host(s4u::Host* host)
{
  host_ = host;
  return *this;
}
SynchroImpl& SynchroImpl::set_timeout(double timeout)
{
  timeout_ = timeout;
  return *this;
}

SynchroImpl* SynchroImpl::start()
{
  model_action_ = host_->get_cpu()->sleep(timeout_);
  model_action_->set_activity(this);
  return this;
}

void SynchroImpl::suspend()
{
  /* The suspension of raw synchros is delayed to when the actor is rescheduled. */
}

void SynchroImpl::resume()
{
  /* I cannot resume raw synchros directly. This is delayed to when the actor is rescheduled at
   * the end of the synchro. */
}

void SynchroImpl::cancel()
{
  /* I cannot cancel raw synchros directly. */
}

void SynchroImpl::set_exception(actor::ActorImpl* issuer)
{
  if (get_state() == State::FAILED) {
    issuer->set_wannadie();
    issuer->exception_ = std::make_exception_ptr(HostFailureException(XBT_THROW_POINT, "Host failed"));
  } else {
    xbt_assert(get_state() == State::SRC_TIMEOUT, "Internal error in SynchroImpl::finish() unexpected synchro state %s",
               get_state_str());
  }
}

void SynchroImpl::finish()
{
  XBT_DEBUG("SynchroImpl::finish() in state %s", get_state_str());
  if (model_action_->get_state() == resource::Action::State::FAILED)
    set_state(State::FAILED);
  else if (model_action_->get_state() == resource::Action::State::FINISHED)
    set_state(State::SRC_TIMEOUT);

  clean_action();

  xbt_assert(simcalls_.size() == 1, "Unexpected number of simcalls waiting: %zu", simcalls_.size());
  actor::Simcall* simcall = simcalls_.front();
  simcalls_.pop_front();

  set_exception(simcall->issuer_);

  finish_callback_();
  simcall->issuer_->waiting_synchro_ = nullptr;
  simcall->issuer_->simcall_answer();
}

} // namespace simgrid::kernel::activity
