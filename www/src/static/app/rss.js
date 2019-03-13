import React from "react";
import {render, findDOMNode} from "react-dom";
import {SelectBox, EditBox, MEditBox, Button, Title, ErrMsg, Hr} from "./feed_component";

const {RssFeed} = require("./spider_pb.js");
const {SpiderRpcClient} = require("./spider_grpc_web_pb.js");


class SubmitForm extends React.Component {
  getInitialState() {
    return {
      category: "",
      url: "",
      item_content_xpath: "",
      removed_xpath_nodes: ["",]
    }
  }

  constructor(props) {
    super(props);
    this.err = null;
    this.submit = this.submit.bind(this);
    this.updateField = this.updateField.bind(this);
    this.state = this.getInitialState();
  }

  submit(e) {
    e.preventDefault();

    let feed = {}
    for (let key in this.state) {
      if (this.state[key].length > 0) {
        feed[key] = this.state[key];
      }
    }
    if (feed["url"] == null || feed["url"] == "") {
      this.err.fadeIn("需要网址数据");
      setTimeout(() => {this.err.fadeOut()}, 800);
    }
    else {
      this.err.fadeIn("正在提交 .....");

      let nodes = feed["removed_xpath_nodes"].filter((e) => {return e != "";});
      if (nodes.length == 0) {
         delete feed["removed_xpath_nodes"];
      }

      let that = this;
      var rpc_url = window.location.protocol + "//" + window.location.hostname;
      if (window.location.protocol == "http") {
        rpc_url = rpc_url + ":80"
      }
      else {
        rpc_url = rpc_url + ":443"
      }
      var client = new SpiderRpcClient(rpc_url);
      var request = new RssFeed();
      request.setUrl(feed["url"]);
      request.setCategory(feed["category"]);
      if (feed["item_content_xpath"] != null && feed["item_content_xpath"] != "") {
        request.setItem_content_xpath(feed["item_content_xpath"]);
      }
      if (feed["removed_xpath_nodes"] != null) {
        request.setRemoved_xpath_nodes(feed["removed_xpath_nodes"]);
      }

      var call = client.submitRssFeed(request, {}, function(err, response){
        if (err) {
          that.err.fadeIn("失败: " + err.message);
          setTimeout(() => {that.err.fadeOut()}, 800);
        }
        else {
          var error = response.getError();
          if (error) {
            that.err.fadeIn("失败: " + response.getMessage());
            setTimeout(() => {that.err.fadeOut()}, 800);
          }
          else{
            that.err.fadeIn("成功");
            setTimeout(() => {that.err.fadeOut()}, 800);
            let state = that.getInitialState();
            state["category"] = that.state.category;
            that.setState(state);
          }
        }
      });
      call.on('status', function(status) {
        that.err.fadeIn(status.details);
      });
    };
    findDOMNode(this.refs.Button).blur();
  }

  updateField(k, v) {
    this.setState({[k]: v});
  }

  render() {
    const style = {
      borderWidth: 0,
      paddingLeft: "36px"
    };

    return (
      <div>
        <ErrMsg ref={(com) => this.err = com} />
        <form onSubmit={this.submit} style={style}>
          <EditBox desc="网址:" updateField={this.updateField} type="url" field="url" value={this.state.url} />
          <SelectBox desc="类别:" updateField={this.updateField} field="category" url="/api/categories" value={this.state.category} />
          <EditBox desc="内容selector[用于非全文输出的feed](选填):" updateField={this.updateField} type="text" field="item_content_xpath" value={this.state.item_content_xpath} />
          <MEditBox desc="清除xpath node 数组(选填):" updateField={this.updateField} type="text" field="removed_xpath_nodes" value={this.state.removed_xpath_nodes} />
          <Button ref="Button"/>
        </form>
      </div>
    )
  }
}

class App extends React.Component {
  render() {
    return (
      <div>
        <Title title="添加订阅源(rss|atom)" />
        <Hr />
        <SubmitForm />
      </div>
    )
  }
}

render(<App />, document.getElementById("content"));
