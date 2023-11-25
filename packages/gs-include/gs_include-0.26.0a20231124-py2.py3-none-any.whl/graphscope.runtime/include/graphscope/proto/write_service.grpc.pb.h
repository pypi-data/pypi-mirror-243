// Generated by the gRPC C++ plugin.
// If you make any local change, they will be lost.
// source: write_service.proto
// Original file comments:
// Copyright 2020 Alibaba Group Holding Limited. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
//
#ifndef GRPC_write_5fservice_2eproto__INCLUDED
#define GRPC_write_5fservice_2eproto__INCLUDED

#include "write_service.pb.h"

#include <functional>
#include <grpcpp/impl/codegen/async_generic_service.h>
#include <grpcpp/impl/codegen/async_stream.h>
#include <grpcpp/impl/codegen/async_unary_call.h>
#include <grpcpp/impl/codegen/client_callback.h>
#include <grpcpp/impl/codegen/client_context.h>
#include <grpcpp/impl/codegen/completion_queue.h>
#include <grpcpp/impl/codegen/message_allocator.h>
#include <grpcpp/impl/codegen/method_handler.h>
#include <grpcpp/impl/codegen/proto_utils.h>
#include <grpcpp/impl/codegen/rpc_method.h>
#include <grpcpp/impl/codegen/server_callback.h>
#include <grpcpp/impl/codegen/server_callback_handlers.h>
#include <grpcpp/impl/codegen/server_context.h>
#include <grpcpp/impl/codegen/service_type.h>
#include <grpcpp/impl/codegen/status.h>
#include <grpcpp/impl/codegen/stub_options.h>
#include <grpcpp/impl/codegen/sync_stream.h>

namespace gs {
namespace rpc {
namespace groot {

class ClientWrite final {
 public:
  static constexpr char const* service_full_name() {
    return "gs.rpc.groot.ClientWrite";
  }
  class StubInterface {
   public:
    virtual ~StubInterface() {}
    virtual ::grpc::Status getClientId(::grpc::ClientContext* context, const ::gs::rpc::groot::GetClientIdRequest& request, ::gs::rpc::groot::GetClientIdResponse* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::GetClientIdResponse>> AsyncgetClientId(::grpc::ClientContext* context, const ::gs::rpc::groot::GetClientIdRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::GetClientIdResponse>>(AsyncgetClientIdRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::GetClientIdResponse>> PrepareAsyncgetClientId(::grpc::ClientContext* context, const ::gs::rpc::groot::GetClientIdRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::GetClientIdResponse>>(PrepareAsyncgetClientIdRaw(context, request, cq));
    }
    virtual ::grpc::Status batchWrite(::grpc::ClientContext* context, const ::gs::rpc::groot::BatchWriteRequest& request, ::gs::rpc::groot::BatchWriteResponse* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::BatchWriteResponse>> AsyncbatchWrite(::grpc::ClientContext* context, const ::gs::rpc::groot::BatchWriteRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::BatchWriteResponse>>(AsyncbatchWriteRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::BatchWriteResponse>> PrepareAsyncbatchWrite(::grpc::ClientContext* context, const ::gs::rpc::groot::BatchWriteRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::BatchWriteResponse>>(PrepareAsyncbatchWriteRaw(context, request, cq));
    }
    virtual ::grpc::Status remoteFlush(::grpc::ClientContext* context, const ::gs::rpc::groot::RemoteFlushRequest& request, ::gs::rpc::groot::RemoteFlushResponse* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::RemoteFlushResponse>> AsyncremoteFlush(::grpc::ClientContext* context, const ::gs::rpc::groot::RemoteFlushRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::RemoteFlushResponse>>(AsyncremoteFlushRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::RemoteFlushResponse>> PrepareAsyncremoteFlush(::grpc::ClientContext* context, const ::gs::rpc::groot::RemoteFlushRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::RemoteFlushResponse>>(PrepareAsyncremoteFlushRaw(context, request, cq));
    }
    class async_interface {
     public:
      virtual ~async_interface() {}
      virtual void getClientId(::grpc::ClientContext* context, const ::gs::rpc::groot::GetClientIdRequest* request, ::gs::rpc::groot::GetClientIdResponse* response, std::function<void(::grpc::Status)>) = 0;
      virtual void getClientId(::grpc::ClientContext* context, const ::gs::rpc::groot::GetClientIdRequest* request, ::gs::rpc::groot::GetClientIdResponse* response, ::grpc::ClientUnaryReactor* reactor) = 0;
      virtual void batchWrite(::grpc::ClientContext* context, const ::gs::rpc::groot::BatchWriteRequest* request, ::gs::rpc::groot::BatchWriteResponse* response, std::function<void(::grpc::Status)>) = 0;
      virtual void batchWrite(::grpc::ClientContext* context, const ::gs::rpc::groot::BatchWriteRequest* request, ::gs::rpc::groot::BatchWriteResponse* response, ::grpc::ClientUnaryReactor* reactor) = 0;
      virtual void remoteFlush(::grpc::ClientContext* context, const ::gs::rpc::groot::RemoteFlushRequest* request, ::gs::rpc::groot::RemoteFlushResponse* response, std::function<void(::grpc::Status)>) = 0;
      virtual void remoteFlush(::grpc::ClientContext* context, const ::gs::rpc::groot::RemoteFlushRequest* request, ::gs::rpc::groot::RemoteFlushResponse* response, ::grpc::ClientUnaryReactor* reactor) = 0;
    };
    typedef class async_interface experimental_async_interface;
    virtual class async_interface* async() { return nullptr; }
    class async_interface* experimental_async() { return async(); }
   private:
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::GetClientIdResponse>* AsyncgetClientIdRaw(::grpc::ClientContext* context, const ::gs::rpc::groot::GetClientIdRequest& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::GetClientIdResponse>* PrepareAsyncgetClientIdRaw(::grpc::ClientContext* context, const ::gs::rpc::groot::GetClientIdRequest& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::BatchWriteResponse>* AsyncbatchWriteRaw(::grpc::ClientContext* context, const ::gs::rpc::groot::BatchWriteRequest& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::BatchWriteResponse>* PrepareAsyncbatchWriteRaw(::grpc::ClientContext* context, const ::gs::rpc::groot::BatchWriteRequest& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::RemoteFlushResponse>* AsyncremoteFlushRaw(::grpc::ClientContext* context, const ::gs::rpc::groot::RemoteFlushRequest& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::gs::rpc::groot::RemoteFlushResponse>* PrepareAsyncremoteFlushRaw(::grpc::ClientContext* context, const ::gs::rpc::groot::RemoteFlushRequest& request, ::grpc::CompletionQueue* cq) = 0;
  };
  class Stub final : public StubInterface {
   public:
    Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options = ::grpc::StubOptions());
    ::grpc::Status getClientId(::grpc::ClientContext* context, const ::gs::rpc::groot::GetClientIdRequest& request, ::gs::rpc::groot::GetClientIdResponse* response) override;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::GetClientIdResponse>> AsyncgetClientId(::grpc::ClientContext* context, const ::gs::rpc::groot::GetClientIdRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::GetClientIdResponse>>(AsyncgetClientIdRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::GetClientIdResponse>> PrepareAsyncgetClientId(::grpc::ClientContext* context, const ::gs::rpc::groot::GetClientIdRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::GetClientIdResponse>>(PrepareAsyncgetClientIdRaw(context, request, cq));
    }
    ::grpc::Status batchWrite(::grpc::ClientContext* context, const ::gs::rpc::groot::BatchWriteRequest& request, ::gs::rpc::groot::BatchWriteResponse* response) override;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::BatchWriteResponse>> AsyncbatchWrite(::grpc::ClientContext* context, const ::gs::rpc::groot::BatchWriteRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::BatchWriteResponse>>(AsyncbatchWriteRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::BatchWriteResponse>> PrepareAsyncbatchWrite(::grpc::ClientContext* context, const ::gs::rpc::groot::BatchWriteRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::BatchWriteResponse>>(PrepareAsyncbatchWriteRaw(context, request, cq));
    }
    ::grpc::Status remoteFlush(::grpc::ClientContext* context, const ::gs::rpc::groot::RemoteFlushRequest& request, ::gs::rpc::groot::RemoteFlushResponse* response) override;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::RemoteFlushResponse>> AsyncremoteFlush(::grpc::ClientContext* context, const ::gs::rpc::groot::RemoteFlushRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::RemoteFlushResponse>>(AsyncremoteFlushRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::RemoteFlushResponse>> PrepareAsyncremoteFlush(::grpc::ClientContext* context, const ::gs::rpc::groot::RemoteFlushRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::RemoteFlushResponse>>(PrepareAsyncremoteFlushRaw(context, request, cq));
    }
    class async final :
      public StubInterface::async_interface {
     public:
      void getClientId(::grpc::ClientContext* context, const ::gs::rpc::groot::GetClientIdRequest* request, ::gs::rpc::groot::GetClientIdResponse* response, std::function<void(::grpc::Status)>) override;
      void getClientId(::grpc::ClientContext* context, const ::gs::rpc::groot::GetClientIdRequest* request, ::gs::rpc::groot::GetClientIdResponse* response, ::grpc::ClientUnaryReactor* reactor) override;
      void batchWrite(::grpc::ClientContext* context, const ::gs::rpc::groot::BatchWriteRequest* request, ::gs::rpc::groot::BatchWriteResponse* response, std::function<void(::grpc::Status)>) override;
      void batchWrite(::grpc::ClientContext* context, const ::gs::rpc::groot::BatchWriteRequest* request, ::gs::rpc::groot::BatchWriteResponse* response, ::grpc::ClientUnaryReactor* reactor) override;
      void remoteFlush(::grpc::ClientContext* context, const ::gs::rpc::groot::RemoteFlushRequest* request, ::gs::rpc::groot::RemoteFlushResponse* response, std::function<void(::grpc::Status)>) override;
      void remoteFlush(::grpc::ClientContext* context, const ::gs::rpc::groot::RemoteFlushRequest* request, ::gs::rpc::groot::RemoteFlushResponse* response, ::grpc::ClientUnaryReactor* reactor) override;
     private:
      friend class Stub;
      explicit async(Stub* stub): stub_(stub) { }
      Stub* stub() { return stub_; }
      Stub* stub_;
    };
    class async* async() override { return &async_stub_; }

   private:
    std::shared_ptr< ::grpc::ChannelInterface> channel_;
    class async async_stub_{this};
    ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::GetClientIdResponse>* AsyncgetClientIdRaw(::grpc::ClientContext* context, const ::gs::rpc::groot::GetClientIdRequest& request, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::GetClientIdResponse>* PrepareAsyncgetClientIdRaw(::grpc::ClientContext* context, const ::gs::rpc::groot::GetClientIdRequest& request, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::BatchWriteResponse>* AsyncbatchWriteRaw(::grpc::ClientContext* context, const ::gs::rpc::groot::BatchWriteRequest& request, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::BatchWriteResponse>* PrepareAsyncbatchWriteRaw(::grpc::ClientContext* context, const ::gs::rpc::groot::BatchWriteRequest& request, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::RemoteFlushResponse>* AsyncremoteFlushRaw(::grpc::ClientContext* context, const ::gs::rpc::groot::RemoteFlushRequest& request, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::gs::rpc::groot::RemoteFlushResponse>* PrepareAsyncremoteFlushRaw(::grpc::ClientContext* context, const ::gs::rpc::groot::RemoteFlushRequest& request, ::grpc::CompletionQueue* cq) override;
    const ::grpc::internal::RpcMethod rpcmethod_getClientId_;
    const ::grpc::internal::RpcMethod rpcmethod_batchWrite_;
    const ::grpc::internal::RpcMethod rpcmethod_remoteFlush_;
  };
  static std::unique_ptr<Stub> NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options = ::grpc::StubOptions());

  class Service : public ::grpc::Service {
   public:
    Service();
    virtual ~Service();
    virtual ::grpc::Status getClientId(::grpc::ServerContext* context, const ::gs::rpc::groot::GetClientIdRequest* request, ::gs::rpc::groot::GetClientIdResponse* response);
    virtual ::grpc::Status batchWrite(::grpc::ServerContext* context, const ::gs::rpc::groot::BatchWriteRequest* request, ::gs::rpc::groot::BatchWriteResponse* response);
    virtual ::grpc::Status remoteFlush(::grpc::ServerContext* context, const ::gs::rpc::groot::RemoteFlushRequest* request, ::gs::rpc::groot::RemoteFlushResponse* response);
  };
  template <class BaseClass>
  class WithAsyncMethod_getClientId : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithAsyncMethod_getClientId() {
      ::grpc::Service::MarkMethodAsync(0);
    }
    ~WithAsyncMethod_getClientId() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status getClientId(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::GetClientIdRequest* /*request*/, ::gs::rpc::groot::GetClientIdResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestgetClientId(::grpc::ServerContext* context, ::gs::rpc::groot::GetClientIdRequest* request, ::grpc::ServerAsyncResponseWriter< ::gs::rpc::groot::GetClientIdResponse>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(0, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithAsyncMethod_batchWrite : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithAsyncMethod_batchWrite() {
      ::grpc::Service::MarkMethodAsync(1);
    }
    ~WithAsyncMethod_batchWrite() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status batchWrite(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::BatchWriteRequest* /*request*/, ::gs::rpc::groot::BatchWriteResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestbatchWrite(::grpc::ServerContext* context, ::gs::rpc::groot::BatchWriteRequest* request, ::grpc::ServerAsyncResponseWriter< ::gs::rpc::groot::BatchWriteResponse>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(1, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithAsyncMethod_remoteFlush : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithAsyncMethod_remoteFlush() {
      ::grpc::Service::MarkMethodAsync(2);
    }
    ~WithAsyncMethod_remoteFlush() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status remoteFlush(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::RemoteFlushRequest* /*request*/, ::gs::rpc::groot::RemoteFlushResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestremoteFlush(::grpc::ServerContext* context, ::gs::rpc::groot::RemoteFlushRequest* request, ::grpc::ServerAsyncResponseWriter< ::gs::rpc::groot::RemoteFlushResponse>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(2, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  typedef WithAsyncMethod_getClientId<WithAsyncMethod_batchWrite<WithAsyncMethod_remoteFlush<Service > > > AsyncService;
  template <class BaseClass>
  class WithCallbackMethod_getClientId : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithCallbackMethod_getClientId() {
      ::grpc::Service::MarkMethodCallback(0,
          new ::grpc::internal::CallbackUnaryHandler< ::gs::rpc::groot::GetClientIdRequest, ::gs::rpc::groot::GetClientIdResponse>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::gs::rpc::groot::GetClientIdRequest* request, ::gs::rpc::groot::GetClientIdResponse* response) { return this->getClientId(context, request, response); }));}
    void SetMessageAllocatorFor_getClientId(
        ::grpc::MessageAllocator< ::gs::rpc::groot::GetClientIdRequest, ::gs::rpc::groot::GetClientIdResponse>* allocator) {
      ::grpc::internal::MethodHandler* const handler = ::grpc::Service::GetHandler(0);
      static_cast<::grpc::internal::CallbackUnaryHandler< ::gs::rpc::groot::GetClientIdRequest, ::gs::rpc::groot::GetClientIdResponse>*>(handler)
              ->SetMessageAllocator(allocator);
    }
    ~WithCallbackMethod_getClientId() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status getClientId(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::GetClientIdRequest* /*request*/, ::gs::rpc::groot::GetClientIdResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerUnaryReactor* getClientId(
      ::grpc::CallbackServerContext* /*context*/, const ::gs::rpc::groot::GetClientIdRequest* /*request*/, ::gs::rpc::groot::GetClientIdResponse* /*response*/)  { return nullptr; }
  };
  template <class BaseClass>
  class WithCallbackMethod_batchWrite : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithCallbackMethod_batchWrite() {
      ::grpc::Service::MarkMethodCallback(1,
          new ::grpc::internal::CallbackUnaryHandler< ::gs::rpc::groot::BatchWriteRequest, ::gs::rpc::groot::BatchWriteResponse>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::gs::rpc::groot::BatchWriteRequest* request, ::gs::rpc::groot::BatchWriteResponse* response) { return this->batchWrite(context, request, response); }));}
    void SetMessageAllocatorFor_batchWrite(
        ::grpc::MessageAllocator< ::gs::rpc::groot::BatchWriteRequest, ::gs::rpc::groot::BatchWriteResponse>* allocator) {
      ::grpc::internal::MethodHandler* const handler = ::grpc::Service::GetHandler(1);
      static_cast<::grpc::internal::CallbackUnaryHandler< ::gs::rpc::groot::BatchWriteRequest, ::gs::rpc::groot::BatchWriteResponse>*>(handler)
              ->SetMessageAllocator(allocator);
    }
    ~WithCallbackMethod_batchWrite() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status batchWrite(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::BatchWriteRequest* /*request*/, ::gs::rpc::groot::BatchWriteResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerUnaryReactor* batchWrite(
      ::grpc::CallbackServerContext* /*context*/, const ::gs::rpc::groot::BatchWriteRequest* /*request*/, ::gs::rpc::groot::BatchWriteResponse* /*response*/)  { return nullptr; }
  };
  template <class BaseClass>
  class WithCallbackMethod_remoteFlush : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithCallbackMethod_remoteFlush() {
      ::grpc::Service::MarkMethodCallback(2,
          new ::grpc::internal::CallbackUnaryHandler< ::gs::rpc::groot::RemoteFlushRequest, ::gs::rpc::groot::RemoteFlushResponse>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::gs::rpc::groot::RemoteFlushRequest* request, ::gs::rpc::groot::RemoteFlushResponse* response) { return this->remoteFlush(context, request, response); }));}
    void SetMessageAllocatorFor_remoteFlush(
        ::grpc::MessageAllocator< ::gs::rpc::groot::RemoteFlushRequest, ::gs::rpc::groot::RemoteFlushResponse>* allocator) {
      ::grpc::internal::MethodHandler* const handler = ::grpc::Service::GetHandler(2);
      static_cast<::grpc::internal::CallbackUnaryHandler< ::gs::rpc::groot::RemoteFlushRequest, ::gs::rpc::groot::RemoteFlushResponse>*>(handler)
              ->SetMessageAllocator(allocator);
    }
    ~WithCallbackMethod_remoteFlush() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status remoteFlush(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::RemoteFlushRequest* /*request*/, ::gs::rpc::groot::RemoteFlushResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerUnaryReactor* remoteFlush(
      ::grpc::CallbackServerContext* /*context*/, const ::gs::rpc::groot::RemoteFlushRequest* /*request*/, ::gs::rpc::groot::RemoteFlushResponse* /*response*/)  { return nullptr; }
  };
  typedef WithCallbackMethod_getClientId<WithCallbackMethod_batchWrite<WithCallbackMethod_remoteFlush<Service > > > CallbackService;
  typedef CallbackService ExperimentalCallbackService;
  template <class BaseClass>
  class WithGenericMethod_getClientId : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithGenericMethod_getClientId() {
      ::grpc::Service::MarkMethodGeneric(0);
    }
    ~WithGenericMethod_getClientId() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status getClientId(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::GetClientIdRequest* /*request*/, ::gs::rpc::groot::GetClientIdResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithGenericMethod_batchWrite : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithGenericMethod_batchWrite() {
      ::grpc::Service::MarkMethodGeneric(1);
    }
    ~WithGenericMethod_batchWrite() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status batchWrite(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::BatchWriteRequest* /*request*/, ::gs::rpc::groot::BatchWriteResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithGenericMethod_remoteFlush : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithGenericMethod_remoteFlush() {
      ::grpc::Service::MarkMethodGeneric(2);
    }
    ~WithGenericMethod_remoteFlush() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status remoteFlush(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::RemoteFlushRequest* /*request*/, ::gs::rpc::groot::RemoteFlushResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithRawMethod_getClientId : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawMethod_getClientId() {
      ::grpc::Service::MarkMethodRaw(0);
    }
    ~WithRawMethod_getClientId() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status getClientId(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::GetClientIdRequest* /*request*/, ::gs::rpc::groot::GetClientIdResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestgetClientId(::grpc::ServerContext* context, ::grpc::ByteBuffer* request, ::grpc::ServerAsyncResponseWriter< ::grpc::ByteBuffer>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(0, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithRawMethod_batchWrite : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawMethod_batchWrite() {
      ::grpc::Service::MarkMethodRaw(1);
    }
    ~WithRawMethod_batchWrite() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status batchWrite(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::BatchWriteRequest* /*request*/, ::gs::rpc::groot::BatchWriteResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestbatchWrite(::grpc::ServerContext* context, ::grpc::ByteBuffer* request, ::grpc::ServerAsyncResponseWriter< ::grpc::ByteBuffer>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(1, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithRawMethod_remoteFlush : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawMethod_remoteFlush() {
      ::grpc::Service::MarkMethodRaw(2);
    }
    ~WithRawMethod_remoteFlush() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status remoteFlush(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::RemoteFlushRequest* /*request*/, ::gs::rpc::groot::RemoteFlushResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestremoteFlush(::grpc::ServerContext* context, ::grpc::ByteBuffer* request, ::grpc::ServerAsyncResponseWriter< ::grpc::ByteBuffer>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(2, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithRawCallbackMethod_getClientId : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawCallbackMethod_getClientId() {
      ::grpc::Service::MarkMethodRawCallback(0,
          new ::grpc::internal::CallbackUnaryHandler< ::grpc::ByteBuffer, ::grpc::ByteBuffer>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::grpc::ByteBuffer* request, ::grpc::ByteBuffer* response) { return this->getClientId(context, request, response); }));
    }
    ~WithRawCallbackMethod_getClientId() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status getClientId(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::GetClientIdRequest* /*request*/, ::gs::rpc::groot::GetClientIdResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerUnaryReactor* getClientId(
      ::grpc::CallbackServerContext* /*context*/, const ::grpc::ByteBuffer* /*request*/, ::grpc::ByteBuffer* /*response*/)  { return nullptr; }
  };
  template <class BaseClass>
  class WithRawCallbackMethod_batchWrite : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawCallbackMethod_batchWrite() {
      ::grpc::Service::MarkMethodRawCallback(1,
          new ::grpc::internal::CallbackUnaryHandler< ::grpc::ByteBuffer, ::grpc::ByteBuffer>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::grpc::ByteBuffer* request, ::grpc::ByteBuffer* response) { return this->batchWrite(context, request, response); }));
    }
    ~WithRawCallbackMethod_batchWrite() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status batchWrite(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::BatchWriteRequest* /*request*/, ::gs::rpc::groot::BatchWriteResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerUnaryReactor* batchWrite(
      ::grpc::CallbackServerContext* /*context*/, const ::grpc::ByteBuffer* /*request*/, ::grpc::ByteBuffer* /*response*/)  { return nullptr; }
  };
  template <class BaseClass>
  class WithRawCallbackMethod_remoteFlush : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawCallbackMethod_remoteFlush() {
      ::grpc::Service::MarkMethodRawCallback(2,
          new ::grpc::internal::CallbackUnaryHandler< ::grpc::ByteBuffer, ::grpc::ByteBuffer>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::grpc::ByteBuffer* request, ::grpc::ByteBuffer* response) { return this->remoteFlush(context, request, response); }));
    }
    ~WithRawCallbackMethod_remoteFlush() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status remoteFlush(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::RemoteFlushRequest* /*request*/, ::gs::rpc::groot::RemoteFlushResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerUnaryReactor* remoteFlush(
      ::grpc::CallbackServerContext* /*context*/, const ::grpc::ByteBuffer* /*request*/, ::grpc::ByteBuffer* /*response*/)  { return nullptr; }
  };
  template <class BaseClass>
  class WithStreamedUnaryMethod_getClientId : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithStreamedUnaryMethod_getClientId() {
      ::grpc::Service::MarkMethodStreamed(0,
        new ::grpc::internal::StreamedUnaryHandler<
          ::gs::rpc::groot::GetClientIdRequest, ::gs::rpc::groot::GetClientIdResponse>(
            [this](::grpc::ServerContext* context,
                   ::grpc::ServerUnaryStreamer<
                     ::gs::rpc::groot::GetClientIdRequest, ::gs::rpc::groot::GetClientIdResponse>* streamer) {
                       return this->StreamedgetClientId(context,
                         streamer);
                  }));
    }
    ~WithStreamedUnaryMethod_getClientId() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable regular version of this method
    ::grpc::Status getClientId(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::GetClientIdRequest* /*request*/, ::gs::rpc::groot::GetClientIdResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    // replace default version of method with streamed unary
    virtual ::grpc::Status StreamedgetClientId(::grpc::ServerContext* context, ::grpc::ServerUnaryStreamer< ::gs::rpc::groot::GetClientIdRequest,::gs::rpc::groot::GetClientIdResponse>* server_unary_streamer) = 0;
  };
  template <class BaseClass>
  class WithStreamedUnaryMethod_batchWrite : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithStreamedUnaryMethod_batchWrite() {
      ::grpc::Service::MarkMethodStreamed(1,
        new ::grpc::internal::StreamedUnaryHandler<
          ::gs::rpc::groot::BatchWriteRequest, ::gs::rpc::groot::BatchWriteResponse>(
            [this](::grpc::ServerContext* context,
                   ::grpc::ServerUnaryStreamer<
                     ::gs::rpc::groot::BatchWriteRequest, ::gs::rpc::groot::BatchWriteResponse>* streamer) {
                       return this->StreamedbatchWrite(context,
                         streamer);
                  }));
    }
    ~WithStreamedUnaryMethod_batchWrite() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable regular version of this method
    ::grpc::Status batchWrite(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::BatchWriteRequest* /*request*/, ::gs::rpc::groot::BatchWriteResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    // replace default version of method with streamed unary
    virtual ::grpc::Status StreamedbatchWrite(::grpc::ServerContext* context, ::grpc::ServerUnaryStreamer< ::gs::rpc::groot::BatchWriteRequest,::gs::rpc::groot::BatchWriteResponse>* server_unary_streamer) = 0;
  };
  template <class BaseClass>
  class WithStreamedUnaryMethod_remoteFlush : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithStreamedUnaryMethod_remoteFlush() {
      ::grpc::Service::MarkMethodStreamed(2,
        new ::grpc::internal::StreamedUnaryHandler<
          ::gs::rpc::groot::RemoteFlushRequest, ::gs::rpc::groot::RemoteFlushResponse>(
            [this](::grpc::ServerContext* context,
                   ::grpc::ServerUnaryStreamer<
                     ::gs::rpc::groot::RemoteFlushRequest, ::gs::rpc::groot::RemoteFlushResponse>* streamer) {
                       return this->StreamedremoteFlush(context,
                         streamer);
                  }));
    }
    ~WithStreamedUnaryMethod_remoteFlush() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable regular version of this method
    ::grpc::Status remoteFlush(::grpc::ServerContext* /*context*/, const ::gs::rpc::groot::RemoteFlushRequest* /*request*/, ::gs::rpc::groot::RemoteFlushResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    // replace default version of method with streamed unary
    virtual ::grpc::Status StreamedremoteFlush(::grpc::ServerContext* context, ::grpc::ServerUnaryStreamer< ::gs::rpc::groot::RemoteFlushRequest,::gs::rpc::groot::RemoteFlushResponse>* server_unary_streamer) = 0;
  };
  typedef WithStreamedUnaryMethod_getClientId<WithStreamedUnaryMethod_batchWrite<WithStreamedUnaryMethod_remoteFlush<Service > > > StreamedUnaryService;
  typedef Service SplitStreamedService;
  typedef WithStreamedUnaryMethod_getClientId<WithStreamedUnaryMethod_batchWrite<WithStreamedUnaryMethod_remoteFlush<Service > > > StreamedService;
};

}  // namespace groot
}  // namespace rpc
}  // namespace gs


#endif  // GRPC_write_5fservice_2eproto__INCLUDED
