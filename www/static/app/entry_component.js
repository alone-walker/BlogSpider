import React from "react";

class Hr extends React.Component {
  render() {
    const style = {
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
}

class Title extends React.Component {
  render() {
    const style = {
      fontFamily: "Nunito, Lantinghei SC, Microsoft YaHei",
      fontSize: "normal",
      fontWeight: "bold",
      textAlign: "center"
    };

    return (
      <div>
        <p style={style}>{this.props.name}</p>
      </div>
    )
  }
}

class Entry extends React.Component {
  render() {
    const style = {
      fontWeight: "600",
      fontSize: "0.9em",
      fontFamily: "Nunito, Lantinghei SC, Microsoft YaHei",
      lineHeight: "2em",
      textDecoration: "none"
    };
    let url = this.props.url;

    return (
      <li>
        <a style={style} href={url} target="_blank">{this.props.title}</a>
      </li>
    )
  }
}

class Entries extends React.Component {
  static defaultProps = {
    prefix: "",
    entries: []
  };

  render() {
    const style = {
      listStyle: "square",
      color: "red",
      marginLeft: "4em"
    };
    let prefix = this.props.prefix;
    let entries = this.props.entries;

    return (
      <ul style={style}>
        {entries.map(function(entry, index) {return <Entry key={index} url={prefix + entry[0]} title={entry[1]} />;})}
      </ul>
    )
  }
}


export {Title, Hr, Entries};
