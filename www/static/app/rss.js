var Title = React.createClass({
	render: function() {
		var style = {
			fontFamily: "Lantinghei SC, Microsoft YaHei, sans-serif",
			fontSize: "1.6em",
			fontWeight: "normal",
			textAlign: "center"
		};

		return (
			<div>
				<p style={style}>{this.props.title}</p>
			</div>
		)
	}
});

var Hr = React.createClass({
	render: function() {
		var style = {
			border: "none",
			height: 1,
			color: "#EEE",
			backgroundColor: "#EEE",
			marginBottom: "1em",
			clear: "both"
		};

		return (
			<hr style={style} />
		)
	}
});

var ErrMsg = React.createClass({
	render: function() {
		var style = {
			textAlign: "center",
			fontSize: "0.5em",
			color: "#888",
			marginBottom: "1em"
		};

		return (
			<div style={style}>
				<span></span>
			</div>
		)
	}
});

var Input = React.createClass({
  handleChange: function(e) {
		var v = e.target.value;
		this.props.updateField(this.props.field, v);
  },

  render: function() {
		var style = {
			backgroundColor: "transparent",
			border: "0.1rem solid #d1d1d1",
			borderRadius: "1px",
			boxShadow: "none",
			boxSizing: "border-box",
			height: "3.2em",
			width: "42em",
			margin: "0em 0em 1.2em 0em",
			display: "block"
		};

    return (
			<input style={style} value={this.props.value} onChange={this.handleChange} type={this.props.type}/>
		)
  }
});

var Label = React.createClass({
	render: function() {
		var style = {
 			fontFamily: "Lantinghei SC, Microsoft YaHei, sans-serif",
			fontSize: "1.0em",
			fontWeight: "normal",
			marginBottom: "0.5em",
			display: "block"
		};

		return (
			<label style={style}>{this.props.desc}</label>
		)
	}
});

var EditBox = React.createClass({
	render: function() {
		return (
			<div>
				<Label desc={this.props.desc} />
				<Input type={this.props.type} updateField={this.props.updateField} field={this.props.field} value={this.props.value} />
			</div>
		)
	}
});

var Select = React.createClass({
	getInitialState: function() {
		return {list: ["null",]};
	},
	
	componentDidMount: function() {
		$.getJSON(this.props.url).done(function(data) {
			var err = data["err"];
			if (!err) {
				var list = data["data"];
				this.setState({list: list});
				this.props.updateField(this.props.field, list[0]);
			}
		}.bind(this));
	},

  handleChange: function(e) {
		var v = e.target.value;
		this.props.updateField(this.props.field, v);
  },

	render: function() {
		var style = {
			backgroundColor: "transparent",
			border: "0.1rem solid #d1d1d1",
			borderRadius: "1px",
			boxShadow: "none",
			boxSizing: "border-box",
			height: "3.2em",
			width: "42em",
			margin: "0em 0em 1.2em 0em",
			display: "block"
		};
		var list = this.state.list;

		return (
			<select style={style} value={this.props.value} onChange={this.handleChange}>
				{list.map(function(v, index) { return <option key={index} value={v}>{v}</option>; })}
			</select>
		)
	}
});

var SelectBox = React.createClass({
	render: function() {
		return (
			<div>
				<Label desc={this.props.desc} />
				<Select updateField={this.props.updateField} url={this.props.url} field={this.props.field} value={this.props.value} />
			</div>
		)
	}
});

var Button = React.createClass({
	render: function() {
		var style = {
			backgroundColor: "transparent",
			border: "0.1rem solid #d1d1d1",
			borderRadius: "0.4rem",
			boxSizing: "borderBox",
			cursor: "pointer",
			display: "inlineBlock",
			fontSize: "0.4rem",
			fontWeight: "700",
			height: "3.2em",
			letterSpacing: "0.3em",
			textAlign: "center",
			textDecoration: "none",
			textTransform: "uppercase",
			whiteSpace: "nowrap"
		};

		return (
			<input style={style} type="submit" value="提交"/>
		)
	}
});


var SubmitForm = React.createClass({
	getInitialState: function(){
		return {category: "",
						url: "",
						content: ""}
	},

	submit: function(e) {
		e.preventDefault();

		var form = this.state;
		if (form["url"] == "") {
			$("span").text("需要网址数据").show().fadeOut(1500);
		}
		else {
			$("span").text("正在提交 .....").show();
			$.ajax({type: "post",
							url: "/api/feed/rss",
							data: form,
							success: function(r){
						 		if (r['err'] == 0) {
									$("span").text("成功").show().fadeOut(1500);
					 			}
				      	else {
									$("span").text("失败: " + r["msg"]).show().fadeOut(1500);
				      	}
								this.setState({url: "", content: ""});
						  }.bind(this)}
			);
		}
		ReactDOM.findDOMNode(this.refs.Submit).blur();
	},

	updateField: function(k, v) {
		this.setState({[k]: v});
	},

	render: function() {
		var style = {
			borderWidth: 0,
			paddingLeft: "36px"
		};

		return (
			<div>
				<ErrMsg />
				<form onSubmit={this.submit} style={style}>
					<EditBox desc="网址:" updateField={this.updateField} type="url" field="url" value={this.state.url} />
					<SelectBox desc="类别:" updateField={this.updateField} field="category" url="/api/categories" value={this.state.category} />
					<EditBox desc="selector[用于非全文输出的feed]:" updateField={this.updateField} type="text" field="content" value={this.state.content} />
					<Button ref="Submit"/>
				</form>
			</div>
		)
	}
});

var App = React.createClass({

	render: function() {
		return (
			<div>
				<Title title="添加订阅源(rss|atom)" />
				<Hr />
				<SubmitForm />
			</div>
		)
	}
});

ReactDOM.render(<App />, document.getElementById('content'));
