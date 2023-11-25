/* Finaliser for a very simple result type
(C) 2017-2023 Niall Douglas <http://www.nedproductions.biz/> (5 commits)
File Created: Oct 2017


Boost Software License - Version 1.0 - August 17th, 2003

Permission is hereby granted, free of charge, to any person or organization
obtaining a copy of the software and accompanying documentation covered by
this license (the "Software") to use, reproduce, display, distribute,
execute, and transmit the Software, and to prepare derivative works of the
Software, and to permit third-parties to whom the Software is furnished to
do so, all subject to the following:

The copyright notices in the Software and this entire statement, including
the above license grant, this restriction and the following disclaimer,
must be included in all copies of the Software, in whole or in part, and
all derivative works of the Software, unless such copies or derivative
works are solely in the form of machine-executable object code generated by
a source language processor.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
*/

#ifndef BOOST_OUTCOME_BASIC_RESULT_FINAL_HPP
#define BOOST_OUTCOME_BASIC_RESULT_FINAL_HPP

#include "basic_result_error_observers.hpp"
#include "basic_result_value_observers.hpp"

BOOST_OUTCOME_V2_NAMESPACE_EXPORT_BEGIN

namespace detail
{
  template <class R, class EC, class NoValuePolicy> using select_basic_result_impl = basic_result_error_observers<basic_result_value_observers<basic_result_storage<R, EC, NoValuePolicy>, R, NoValuePolicy>, EC, NoValuePolicy>;

  template <class R, class S, class NoValuePolicy>
  class basic_result_final
#if defined(BOOST_OUTCOME_DOXYGEN_IS_IN_THE_HOUSE)
  : public basic_result_error_observers<basic_result_value_observers<basic_result_storage<R, S, NoValuePolicy>, R, NoValuePolicy>, S, NoValuePolicy>
#else
  : public select_basic_result_impl<R, S, NoValuePolicy>
#endif
  {
    using base = select_basic_result_impl<R, S, NoValuePolicy>;

  public:
    using base::base;

    constexpr explicit operator bool() const noexcept { return this->_state._status.have_value(); }
    constexpr bool has_value() const noexcept { return this->_state._status.have_value(); }
    constexpr bool has_error() const noexcept { return this->_state._status.have_error(); }
    constexpr bool has_exception() const noexcept { return this->_state._status.have_exception(); }
    constexpr bool has_lost_consistency() const noexcept { return this->_state._status.have_lost_consistency(); }
    constexpr bool has_failure() const noexcept { return this->_state._status.have_error() || this->_state._status.have_exception(); }

    BOOST_OUTCOME_TEMPLATE(class T, class U, class V)
    BOOST_OUTCOME_TREQUIRES(BOOST_OUTCOME_TEXPR(std::declval<detail::devoid<R>>() == std::declval<detail::devoid<T>>()),  //
                      BOOST_OUTCOME_TEXPR(std::declval<detail::devoid<S>>() == std::declval<detail::devoid<U>>()))
    constexpr bool operator==(const basic_result_final<T, U, V> &o) const noexcept(  //
    noexcept(std::declval<detail::devoid<R>>() == std::declval<detail::devoid<T>>()) && noexcept(std::declval<detail::devoid<S>>() == std::declval<detail::devoid<U>>()))
    {
      if(this->_state._status.have_value() && o._state._status.have_value())
      {
        return this->_state._value == o._state._value;  // NOLINT
      }
      if(this->_state._status.have_error() && o._state._status.have_error())
      {
        return this->_state._error == o._state._error;
      }
      return false;
    }
    BOOST_OUTCOME_TEMPLATE(class T)
    BOOST_OUTCOME_TREQUIRES(BOOST_OUTCOME_TEXPR(std::declval<R>() == std::declval<T>()))
    constexpr bool operator==(const success_type<T> &o) const noexcept(  //
    noexcept(std::declval<R>() == std::declval<T>()))
    {
      if(this->_state._status.have_value())
      {
        return this->_state._value == o.value();
      }
      return false;
    }
    constexpr bool operator==(const success_type<void> &o) const noexcept
    {
      (void) o;
      return this->_state._status.have_value();
    }
    BOOST_OUTCOME_TEMPLATE(class T)
    BOOST_OUTCOME_TREQUIRES(BOOST_OUTCOME_TEXPR(std::declval<S>() == std::declval<T>()))
    constexpr bool operator==(const failure_type<T, void> &o) const noexcept(  //
    noexcept(std::declval<S>() == std::declval<T>()))
    {
      if(this->_state._status.have_error())
      {
        return this->_state._error == o.error();
      }
      return false;
    }
    BOOST_OUTCOME_TEMPLATE(class T, class U, class V)
    BOOST_OUTCOME_TREQUIRES(BOOST_OUTCOME_TEXPR(std::declval<detail::devoid<R>>() != std::declval<detail::devoid<T>>()),  //
                      BOOST_OUTCOME_TEXPR(std::declval<detail::devoid<S>>() != std::declval<detail::devoid<U>>()))
    constexpr bool operator!=(const basic_result_final<T, U, V> &o) const noexcept(  //
    noexcept(std::declval<detail::devoid<R>>() != std::declval<detail::devoid<T>>()) && noexcept(std::declval<detail::devoid<S>>() != std::declval<detail::devoid<U>>()))
    {
      if(this->_state._status.have_value() && o._state._status.have_value())
      {
        return this->_state._value != o._state._value;
      }
      if(this->_state._status.have_error() && o._state._status.have_error())
      {
        return this->_state._error != o._state._error;
      }
      return true;
    }
    BOOST_OUTCOME_TEMPLATE(class T)
    BOOST_OUTCOME_TREQUIRES(BOOST_OUTCOME_TEXPR(std::declval<R>() != std::declval<T>()))
    constexpr bool operator!=(const success_type<T> &o) const noexcept(  //
    noexcept(std::declval<R>() != std::declval<T>()))
    {
      if(this->_state._status.have_value())
      {
        return this->_state._value != o.value();
      }
      return false;
    }
    constexpr bool operator!=(const success_type<void> &o) const noexcept
    {
      (void) o;
      return !this->_state._status.have_value();
    }
    BOOST_OUTCOME_TEMPLATE(class T)
    BOOST_OUTCOME_TREQUIRES(BOOST_OUTCOME_TEXPR(std::declval<S>() != std::declval<T>()))
    constexpr bool operator!=(const failure_type<T, void> &o) const noexcept(  //
    noexcept(std::declval<S>() != std::declval<T>()))
    {
      if(this->_state._status.have_error())
      {
        return this->_state._error != o.error();
      }
      return true;
    }
  };
  template <class T, class U, class V, class W> constexpr inline bool operator==(const success_type<W> &a, const basic_result_final<T, U, V> &b) noexcept(noexcept(b == a)) { return b == a; }
  template <class T, class U, class V, class W> constexpr inline bool operator==(const failure_type<W, void> &a, const basic_result_final<T, U, V> &b) noexcept(noexcept(b == a)) { return b == a; }
  template <class T, class U, class V, class W> constexpr inline bool operator!=(const success_type<W> &a, const basic_result_final<T, U, V> &b) noexcept(noexcept(b == a)) { return b != a; }
  template <class T, class U, class V, class W> constexpr inline bool operator!=(const failure_type<W, void> &a, const basic_result_final<T, U, V> &b) noexcept(noexcept(b == a)) { return b != a; }
}  // namespace detail

BOOST_OUTCOME_V2_NAMESPACE_END

#endif
