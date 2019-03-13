/**
 * @fileoverview gRPC-Web generated client stub for spiderrpc
 * @enhanceable
 * @public
 */

// GENERATED CODE -- DO NOT EDIT!



const grpc = {};
grpc.web = require('grpc-web');

const proto = {};
proto.spiderrpc = require('./spider_pb.js');

/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.spiderrpc.SpiderRpcClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

  /**
   * @private @const {?Object} The credentials to be used to connect
   *    to the server
   */
  this.credentials_ = credentials;

  /**
   * @private @const {?Object} Options for the client
   */
  this.options_ = options;
};


/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.spiderrpc.SpiderRpcPromiseClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!proto.spiderrpc.SpiderRpcClient} The delegate callback based client
   */
  this.delegateClient_ = new proto.spiderrpc.SpiderRpcClient(
      hostname, credentials, options);

};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.spiderrpc.RssFeed,
 *   !proto.spiderrpc.SubmitResult>}
 */
const methodInfo_SpiderRpc_SubmitRssFeed = new grpc.web.AbstractClientBase.MethodInfo(
  proto.spiderrpc.SubmitResult,
  /** @param {!proto.spiderrpc.RssFeed} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.spiderrpc.SubmitResult.deserializeBinary
);


/**
 * @param {!proto.spiderrpc.RssFeed} request The
 *     request proto
 * @param {!Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.spiderrpc.SubmitResult)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.spiderrpc.SubmitResult>|undefined}
 *     The XHR Node Readable Stream
 */
proto.spiderrpc.SpiderRpcClient.prototype.submitRssFeed =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/spiderrpc.SpiderRpc/SubmitRssFeed',
      request,
      metadata,
      methodInfo_SpiderRpc_SubmitRssFeed,
      callback);
};


/**
 * @param {!proto.spiderrpc.RssFeed} request The
 *     request proto
 * @param {!Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.spiderrpc.SubmitResult>}
 *     The XHR Node Readable Stream
 */
proto.spiderrpc.SpiderRpcPromiseClient.prototype.submitRssFeed =
    function(request, metadata) {
  return new Promise((resolve, reject) => {
    this.delegateClient_.submitRssFeed(
      request, metadata, (error, response) => {
        error ? reject(error) : resolve(response);
      });
  });
};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.spiderrpc.BlogFeed,
 *   !proto.spiderrpc.SubmitResult>}
 */
const methodInfo_SpiderRpc_SubmitBlogFeed = new grpc.web.AbstractClientBase.MethodInfo(
  proto.spiderrpc.SubmitResult,
  /** @param {!proto.spiderrpc.BlogFeed} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.spiderrpc.SubmitResult.deserializeBinary
);


/**
 * @param {!proto.spiderrpc.BlogFeed} request The
 *     request proto
 * @param {!Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.spiderrpc.SubmitResult)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.spiderrpc.SubmitResult>|undefined}
 *     The XHR Node Readable Stream
 */
proto.spiderrpc.SpiderRpcClient.prototype.submitBlogFeed =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/spiderrpc.SpiderRpc/SubmitBlogFeed',
      request,
      metadata,
      methodInfo_SpiderRpc_SubmitBlogFeed,
      callback);
};


/**
 * @param {!proto.spiderrpc.BlogFeed} request The
 *     request proto
 * @param {!Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.spiderrpc.SubmitResult>}
 *     The XHR Node Readable Stream
 */
proto.spiderrpc.SpiderRpcPromiseClient.prototype.submitBlogFeed =
    function(request, metadata) {
  return new Promise((resolve, reject) => {
    this.delegateClient_.submitBlogFeed(
      request, metadata, (error, response) => {
        error ? reject(error) : resolve(response);
      });
  });
};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.spiderrpc.SpiderList,
 *   !proto.spiderrpc.CrawlTaskResult>}
 */
const methodInfo_SpiderRpc_CrawlArticles = new grpc.web.AbstractClientBase.MethodInfo(
  proto.spiderrpc.CrawlTaskResult,
  /** @param {!proto.spiderrpc.SpiderList} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.spiderrpc.CrawlTaskResult.deserializeBinary
);


/**
 * @param {!proto.spiderrpc.SpiderList} request The
 *     request proto
 * @param {!Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.spiderrpc.CrawlTaskResult)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.spiderrpc.CrawlTaskResult>|undefined}
 *     The XHR Node Readable Stream
 */
proto.spiderrpc.SpiderRpcClient.prototype.crawlArticles =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/spiderrpc.SpiderRpc/CrawlArticles',
      request,
      metadata,
      methodInfo_SpiderRpc_CrawlArticles,
      callback);
};


/**
 * @param {!proto.spiderrpc.SpiderList} request The
 *     request proto
 * @param {!Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.spiderrpc.CrawlTaskResult>}
 *     The XHR Node Readable Stream
 */
proto.spiderrpc.SpiderRpcPromiseClient.prototype.crawlArticles =
    function(request, metadata) {
  return new Promise((resolve, reject) => {
    this.delegateClient_.crawlArticles(
      request, metadata, (error, response) => {
        error ? reject(error) : resolve(response);
      });
  });
};


module.exports = proto.spiderrpc;

