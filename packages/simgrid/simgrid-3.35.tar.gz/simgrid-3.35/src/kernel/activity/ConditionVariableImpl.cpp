/* Copyright (c) 2007-2023. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "src/kernel/activity/ConditionVariableImpl.hpp"
#include "src/kernel/activity/MutexImpl.hpp"
#include "src/kernel/activity/Synchro.hpp"
#include "src/kernel/actor/SynchroObserver.hpp"
#include <cmath> // std::isfinite

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(ker_condition, ker_synchro, "Condition variables kernel-space implementation");

/********************************* Condition **********************************/

namespace simgrid::kernel::activity {

/**
 * @brief Signalizes a condition.
 *
 * Signalizes a condition and wakes up a sleeping actor.
 * If there are no actor sleeping, no action is done.
 */
void ConditionVariableImpl::signal()
{
  XBT_DEBUG("Signal condition %p", this);

  /* If there are actors waiting for the condition choose one and try to make it acquire the mutex */
  if (not sleeping_.empty()) {
    auto& proc = sleeping_.front();
    sleeping_.pop_front();

    /* Destroy waiter's synchronization */
    proc.waiting_synchro_ = nullptr;

    /* Now transform the cond wait simcall into a mutex lock one */
    actor::Simcall* simcall = &proc.simcall_;
    const auto* observer    = dynamic_cast<kernel::actor::ConditionVariableObserver*>(simcall->observer_);
    xbt_assert(observer != nullptr);
    observer->get_mutex()->lock_async(simcall->issuer_)->wait_for(simcall->issuer_, -1);
  }
  XBT_OUT();
}

/**
 * @brief Broadcasts a condition.
 *
 * Signal ALL actors waiting on a condition.
 * If there are no actor waiting, no action is done.
 */
void ConditionVariableImpl::broadcast()
{
  XBT_DEBUG("Broadcast condition %p", this);

  /* Signal the condition until nobody is waiting on it */
  while (not sleeping_.empty())
    signal();
}

void ConditionVariableImpl::wait(MutexImpl* mutex, double timeout, actor::ActorImpl* issuer)
{
  XBT_DEBUG("Wait condition %p", this);
  xbt_assert(std::isfinite(timeout), "timeout is not finite!");

  /* Unlock the provided mutex (the simcall observer ensures that one is provided, no need to check) */
  auto* owner = mutex->get_owner();
  xbt_assert(owner == issuer,
             "Actor %s cannot wait on ConditionVariable %p since it does not own the provided mutex %p (which is "
             "owned by %s).",
             issuer->get_cname(), this, mutex, (owner == nullptr ? "nobody" : owner->get_cname()));
  mutex_ = mutex;
  mutex->unlock(issuer);

  SynchroImplPtr synchro(new SynchroImpl([this, issuer]() {
    this->remove_sleeping_actor(*issuer);
    auto* observer = dynamic_cast<kernel::actor::ConditionVariableObserver*>(issuer->simcall_.observer_);
    xbt_assert(observer != nullptr);
    observer->set_result(true);
  }));
  synchro->set_host(issuer->get_host()).set_timeout(timeout).start();
  synchro->register_simcall(&issuer->simcall_);
  sleeping_.push_back(*issuer);
}

// boost::intrusive_ptr<ConditionVariableImpl> support:
void intrusive_ptr_add_ref(ConditionVariableImpl* cond)
{
  cond->refcount_.fetch_add(1, std::memory_order_relaxed);
}

void intrusive_ptr_release(ConditionVariableImpl* cond)
{
  if (cond->refcount_.fetch_sub(1, std::memory_order_release) == 1) {
    std::atomic_thread_fence(std::memory_order_acquire);
    xbt_assert(cond->sleeping_.empty(), "Cannot destroy conditional since someone is still using it");
    delete cond;
  }
}
} // namespace simgrid::kernel::activity
