(function (z, W) {
  typeof exports == "object" && typeof module < "u"
    ? W(
        exports,
        require("@graphiql/react"),
        require("react"),
        require("graphql"),
      )
    : typeof define == "function" && define.amd
      ? define(["exports", "@graphiql/react", "react", "graphql"], W)
      : ((z = typeof globalThis < "u" ? globalThis : z || self),
        W(
          (z.GraphiQLPluginExplorer = {}),
          z.GraphiQL.React,
          z.React,
          z.GraphiQL.GraphQL,
        ));
})(this, function (z, W, N, De) {
  "use strict";
  function ve(i) {
    const t = Object.create(null, {
      [Symbol.toStringTag]: { value: "Module" },
    });
    if (i) {
      for (const s in i)
        if (s !== "default") {
          const n = Object.getOwnPropertyDescriptor(i, s);
          Object.defineProperty(
            t,
            s,
            n.get ? n : { enumerable: !0, get: () => i[s] },
          );
        }
    }
    return (t.default = i), Object.freeze(t);
  }
  const Te = ve(N),
    Ne = ve(De);
  function ge(i) {
    return i &&
      Object.prototype.hasOwnProperty.call(i, "default") &&
      Object.keys(i).length === 1
      ? i.default
      : i;
  }
  var re = {},
    ie = {};
  const Le = ge(Te),
    Me = ge(Ne);
  Object.defineProperty(ie, "__esModule", { value: !0 });
  var je =
      typeof Symbol == "function" && typeof Symbol.iterator == "symbol"
        ? function (i) {
            return typeof i;
          }
        : function (i) {
            return i &&
              typeof Symbol == "function" &&
              i.constructor === Symbol &&
              i !== Symbol.prototype
              ? "symbol"
              : typeof i;
          },
    ye = (function () {
      function i(t, s) {
        var n = [],
          e = !0,
          l = !1,
          c = void 0;
        try {
          for (
            var f = t[Symbol.iterator](), u;
            !(e = (u = f.next()).done) &&
            (n.push(u.value), !(s && n.length === s));
            e = !0
          );
        } catch (r) {
          (l = !0), (c = r);
        } finally {
          try {
            !e && f.return && f.return();
          } finally {
            if (l) throw c;
          }
        }
        return n;
      }
      return function (t, s) {
        if (Array.isArray(t)) return t;
        if (Symbol.iterator in Object(t)) return i(t, s);
        throw new TypeError(
          "Invalid attempt to destructure non-iterable instance",
        );
      };
    })(),
    k =
      Object.assign ||
      function (i) {
        for (var t = 1; t < arguments.length; t++) {
          var s = arguments[t];
          for (var n in s)
            Object.prototype.hasOwnProperty.call(s, n) && (i[n] = s[n]);
        }
        return i;
      },
    P = (function () {
      function i(t, s) {
        for (var n = 0; n < s.length; n++) {
          var e = s[n];
          (e.enumerable = e.enumerable || !1),
            (e.configurable = !0),
            "value" in e && (e.writable = !0),
            Object.defineProperty(t, e.key, e);
        }
      }
      return function (t, s, n) {
        return s && i(t.prototype, s), n && i(t, n), t;
      };
    })();
  ie.defaultValue = ue;
  var Ie = Le,
    a = Pe(Ie),
    v = Me;
  function Pe(i) {
    if (i && i.__esModule) return i;
    var t = {};
    if (i != null)
      for (var s in i)
        Object.prototype.hasOwnProperty.call(i, s) && (t[s] = i[s]);
    return (t.default = i), t;
  }
  function he(i, t, s) {
    return (
      t in i
        ? Object.defineProperty(i, t, {
            value: s,
            enumerable: !0,
            configurable: !0,
            writable: !0,
          })
        : (i[t] = s),
      i
    );
  }
  function I(i) {
    if (Array.isArray(i)) {
      for (var t = 0, s = Array(i.length); t < i.length; t++) s[t] = i[t];
      return s;
    } else return Array.from(i);
  }
  function q(i, t) {
    if (!(i instanceof t))
      throw new TypeError("Cannot call a class as a function");
  }
  function w(i, t) {
    if (!i)
      throw new ReferenceError(
        "this hasn't been initialised - super() hasn't been called",
      );
    return t && (typeof t == "object" || typeof t == "function") ? t : i;
  }
  function R(i, t) {
    if (typeof t != "function" && t !== null)
      throw new TypeError(
        "Super expression must either be null or a function, not " + typeof t,
      );
    (i.prototype = Object.create(t && t.prototype, {
      constructor: { value: i, enumerable: !1, writable: !0, configurable: !0 },
    })),
      t &&
        (Object.setPrototypeOf
          ? Object.setPrototypeOf(i, t)
          : (i.__proto__ = t));
  }
  function se(i) {
    return i.charAt(0).toUpperCase() + i.slice(1);
  }
  var qe = {
      keyword: "#B11A04",
      def: "#D2054E",
      property: "#1F61A0",
      qualifier: "#1C92A9",
      attribute: "#8B2BB9",
      number: "#2882F9",
      string: "#D64292",
      builtin: "#D47509",
      string2: "#0B7FC7",
      variable: "#397D13",
      atom: "#CA9800",
    },
    Re = a.createElement(
      "svg",
      { width: "12", height: "9" },
      a.createElement("path", { fill: "#666", d: "M 0 2 L 9 2 L 4.5 7.5 z" }),
    ),
    Be = a.createElement(
      "svg",
      { width: "12", height: "9" },
      a.createElement("path", { fill: "#666", d: "M 0 0 L 0 9 L 5.5 4.5 z" }),
    ),
    Ue = a.createElement(
      "svg",
      {
        style: { marginRight: "3px", marginLeft: "-3px" },
        width: "12",
        height: "12",
        viewBox: "0 0 18 18",
        fill: "none",
        xmlns: "http://www.w3.org/2000/svg",
      },
      a.createElement("path", {
        d: "M16 0H2C0.9 0 0 0.9 0 2V16C0 17.1 0.9 18 2 18H16C17.1 18 18 17.1 18 16V2C18 0.9 17.1 0 16 0ZM16 16H2V2H16V16ZM14.99 6L13.58 4.58L6.99 11.17L4.41 8.6L2.99 10.01L6.99 14L14.99 6Z",
        fill: "#666",
      }),
    ),
    He = a.createElement(
      "svg",
      {
        style: { marginRight: "3px", marginLeft: "-3px" },
        width: "12",
        height: "12",
        viewBox: "0 0 18 18",
        fill: "none",
        xmlns: "http://www.w3.org/2000/svg",
      },
      a.createElement("path", {
        d: "M16 2V16H2V2H16ZM16 0H2C0.9 0 0 0.9 0 2V16C0 17.1 0.9 18 2 18H16C17.1 18 18 17.1 18 16V2C18 0.9 17.1 0 16 0Z",
        fill: "#CCC",
      }),
    );
  function ae(i) {
    return i.checked
      ? i.styleConfig.checkboxChecked
      : i.styleConfig.checkboxUnchecked;
  }
  function be(i) {
    var t = i.getFields();
    if (t.id) {
      var s = ["id"];
      return t.email ? s.push("email") : t.name && s.push("name"), s;
    }
    if (t.edges) return ["edges"];
    if (t.node) return ["node"];
    if (t.nodes) return ["nodes"];
    var n = [];
    return (
      Object.keys(t).forEach(function (e) {
        (0, v.isLeafType)(t[e].type) && n.push(e);
      }),
      n.length ? n.slice(0, 2) : ["__typename"]
    );
  }
  function Se(i) {
    return (0, v.isNonNullType)(i.type) && i.defaultValue === void 0;
  }
  function ze(i) {
    for (var t = i; (0, v.isWrappingType)(t); ) t = t.ofType;
    return t;
  }
  function Q(i) {
    for (var t = i; (0, v.isWrappingType)(t); ) t = t.ofType;
    return t;
  }
  function ke(i, t) {
    if (typeof t != "string" && t.kind === "VariableDefinition")
      return t.variable;
    if ((0, v.isScalarType)(i))
      try {
        switch (i.name) {
          case "String":
            return { kind: "StringValue", value: String(i.parseValue(t)) };
          case "Float":
            return {
              kind: "FloatValue",
              value: String(i.parseValue(parseFloat(t))),
            };
          case "Int":
            return {
              kind: "IntValue",
              value: String(i.parseValue(parseInt(t, 10))),
            };
          case "Boolean":
            try {
              var s = JSON.parse(t);
              return typeof s == "boolean"
                ? { kind: "BooleanValue", value: s }
                : { kind: "BooleanValue", value: !1 };
            } catch {
              return { kind: "BooleanValue", value: !1 };
            }
          default:
            return { kind: "StringValue", value: String(i.parseValue(t)) };
        }
      } catch (e) {
        return (
          console.error("error coercing arg value", e, t),
          { kind: "StringValue", value: t }
        );
      }
    else
      try {
        var n = i.parseValue(t);
        return n
          ? { kind: "EnumValue", value: String(n) }
          : { kind: "EnumValue", value: i.getValues()[0].name };
      } catch {
        return { kind: "EnumValue", value: i.getValues()[0].name };
      }
  }
  var Ge = (function (i) {
    R(t, i);
    function t() {
      var s, n, e, l;
      q(this, t);
      for (var c = arguments.length, f = Array(c), u = 0; u < c; u++)
        f[u] = arguments[u];
      return (
        (l =
          ((n =
            ((e = w(
              this,
              (s = t.__proto__ || Object.getPrototypeOf(t)).call.apply(
                s,
                [this].concat(f),
              ),
            )),
            e)),
          (e._getArgSelection = function () {
            return e.props.selection.fields.find(function (r) {
              return r.name.value === e.props.arg.name;
            });
          }),
          (e._removeArg = function () {
            var r = e.props.selection,
              o = e._getArgSelection();
            (e._previousArgSelection = o),
              e.props.modifyFields(
                r.fields.filter(function (p) {
                  return p !== o;
                }),
                !0,
              );
          }),
          (e._addArg = function () {
            var r = e.props,
              o = r.selection,
              p = r.arg,
              m = r.getDefaultScalarArgValue,
              h = r.parentField,
              F = r.makeDefaultArg,
              d = Q(p.type),
              b = null;
            if (e._previousArgSelection) b = e._previousArgSelection;
            else if ((0, v.isInputObjectType)(d)) {
              var g = d.getFields();
              b = {
                kind: "ObjectField",
                name: { kind: "Name", value: p.name },
                value: {
                  kind: "ObjectValue",
                  fields: oe(
                    m,
                    F,
                    h,
                    Object.keys(g).map(function (C) {
                      return g[C];
                    }),
                  ),
                },
              };
            } else
              (0, v.isLeafType)(d) &&
                (b = {
                  kind: "ObjectField",
                  name: { kind: "Name", value: p.name },
                  value: m(h, p, d),
                });
            if (!b) console.error("Unable to add arg for argType", d);
            else
              return e.props.modifyFields(
                [].concat(I(o.fields || []), [b]),
                !0,
              );
          }),
          (e._setArgValue = function (r, o) {
            var p = !1,
              m = !1,
              h = !1;
            try {
              r.kind === "VariableDefinition"
                ? (m = !0)
                : r === null || typeof r > "u"
                  ? (p = !0)
                  : typeof r.kind == "string" && (h = !0);
            } catch {}
            var F = e.props.selection,
              d = e._getArgSelection();
            if (!d) {
              console.error("missing arg selection when setting arg value");
              return;
            }
            var b = Q(e.props.arg.type),
              g = (0, v.isLeafType)(b) || m || p || h;
            if (!g) {
              console.warn(
                "Unable to handle non leaf types in InputArgView.setArgValue",
                r,
              );
              return;
            }
            var C = void 0,
              _ = void 0;
            r === null || typeof r > "u"
              ? (_ = null)
              : !r.target && r.kind && r.kind === "VariableDefinition"
                ? ((C = r), (_ = C.variable))
                : typeof r.kind == "string"
                  ? (_ = r)
                  : r.target &&
                    typeof r.target.value == "string" &&
                    ((C = r.target.value), (_ = ke(b, C)));
            var A = e.props.modifyFields(
              (F.fields || []).map(function (D) {
                var B = D === d,
                  j = B ? k({}, D, { value: _ }) : D;
                return j;
              }),
              o,
            );
            return A;
          }),
          (e._modifyChildFields = function (r) {
            return e.props.modifyFields(
              e.props.selection.fields.map(function (o) {
                return o.name.value === e.props.arg.name
                  ? k({}, o, { value: { kind: "ObjectValue", fields: r } })
                  : o;
              }),
              !0,
            );
          }),
          n)),
        w(e, l)
      );
    }
    return (
      P(t, [
        {
          key: "render",
          value: function () {
            var n = this.props,
              e = n.arg,
              l = n.parentField,
              c = this._getArgSelection();
            return a.createElement(Ee, {
              argValue: c ? c.value : null,
              arg: e,
              parentField: l,
              addArg: this._addArg,
              removeArg: this._removeArg,
              setArgFields: this._modifyChildFields,
              setArgValue: this._setArgValue,
              getDefaultScalarArgValue: this.props.getDefaultScalarArgValue,
              makeDefaultArg: this.props.makeDefaultArg,
              onRunOperation: this.props.onRunOperation,
              styleConfig: this.props.styleConfig,
              onCommit: this.props.onCommit,
              definition: this.props.definition,
            });
          },
        },
      ]),
      t
    );
  })(a.PureComponent);
  function ue(i) {
    if ((0, v.isEnumType)(i))
      return { kind: "EnumValue", value: i.getValues()[0].name };
    switch (i.name) {
      case "String":
        return { kind: "StringValue", value: "" };
      case "Float":
        return { kind: "FloatValue", value: "1.5" };
      case "Int":
        return { kind: "IntValue", value: "10" };
      case "Boolean":
        return { kind: "BooleanValue", value: !1 };
      default:
        return { kind: "StringValue", value: "" };
    }
  }
  function Ce(i, t, s) {
    return ue(s);
  }
  var We = (function (i) {
    R(t, i);
    function t() {
      var s, n, e, l;
      q(this, t);
      for (var c = arguments.length, f = Array(c), u = 0; u < c; u++)
        f[u] = arguments[u];
      return (
        (l =
          ((n =
            ((e = w(
              this,
              (s = t.__proto__ || Object.getPrototypeOf(t)).call.apply(
                s,
                [this].concat(f),
              ),
            )),
            e)),
          (e._getArgSelection = function () {
            var r = e.props.selection;
            return (r.arguments || []).find(function (o) {
              return o.name.value === e.props.arg.name;
            });
          }),
          (e._removeArg = function (r) {
            var o = e.props.selection,
              p = e._getArgSelection();
            return (
              (e._previousArgSelection = p),
              e.props.modifyArguments(
                (o.arguments || []).filter(function (m) {
                  return m !== p;
                }),
                r,
              )
            );
          }),
          (e._addArg = function (r) {
            var o = e.props,
              p = o.selection,
              m = o.getDefaultScalarArgValue,
              h = o.makeDefaultArg,
              F = o.parentField,
              d = o.arg,
              b = Q(d.type),
              g = null;
            if (e._previousArgSelection) g = e._previousArgSelection;
            else if ((0, v.isInputObjectType)(b)) {
              var C = b.getFields();
              g = {
                kind: "Argument",
                name: { kind: "Name", value: d.name },
                value: {
                  kind: "ObjectValue",
                  fields: oe(
                    m,
                    h,
                    F,
                    Object.keys(C).map(function (_) {
                      return C[_];
                    }),
                  ),
                },
              };
            } else
              (0, v.isLeafType)(b) &&
                (g = {
                  kind: "Argument",
                  name: { kind: "Name", value: d.name },
                  value: m(F, d, b),
                });
            return g
              ? e.props.modifyArguments([].concat(I(p.arguments || []), [g]), r)
              : (console.error("Unable to add arg for argType", b), null);
          }),
          (e._setArgValue = function (r, o) {
            var p = !1,
              m = !1,
              h = !1;
            try {
              r.kind === "VariableDefinition"
                ? (m = !0)
                : r === null || typeof r > "u"
                  ? (p = !0)
                  : typeof r.kind == "string" && (h = !0);
            } catch {}
            var F = e.props.selection,
              d = e._getArgSelection();
            if (!d && !m) {
              console.error("missing arg selection when setting arg value");
              return;
            }
            var b = Q(e.props.arg.type),
              g = (0, v.isLeafType)(b) || m || p || h;
            if (!g) {
              console.warn(
                "Unable to handle non leaf types in ArgView._setArgValue",
              );
              return;
            }
            var C = void 0,
              _ = void 0;
            return (
              r === null || typeof r > "u"
                ? (_ = null)
                : r.target && typeof r.target.value == "string"
                  ? ((C = r.target.value), (_ = ke(b, C)))
                  : !r.target && r.kind === "VariableDefinition"
                    ? ((C = r), (_ = C.variable))
                    : typeof r.kind == "string" && (_ = r),
              e.props.modifyArguments(
                (F.arguments || []).map(function (A) {
                  return A === d ? k({}, A, { value: _ }) : A;
                }),
                o,
              )
            );
          }),
          (e._setArgFields = function (r, o) {
            var p = e.props.selection,
              m = e._getArgSelection();
            if (!m) {
              console.error("missing arg selection when setting arg value");
              return;
            }
            return e.props.modifyArguments(
              (p.arguments || []).map(function (h) {
                return h === m
                  ? k({}, h, { value: { kind: "ObjectValue", fields: r } })
                  : h;
              }),
              o,
            );
          }),
          n)),
        w(e, l)
      );
    }
    return (
      P(t, [
        {
          key: "render",
          value: function () {
            var n = this.props,
              e = n.arg,
              l = n.parentField,
              c = this._getArgSelection();
            return a.createElement(Ee, {
              argValue: c ? c.value : null,
              arg: e,
              parentField: l,
              addArg: this._addArg,
              removeArg: this._removeArg,
              setArgFields: this._setArgFields,
              setArgValue: this._setArgValue,
              getDefaultScalarArgValue: this.props.getDefaultScalarArgValue,
              makeDefaultArg: this.props.makeDefaultArg,
              onRunOperation: this.props.onRunOperation,
              styleConfig: this.props.styleConfig,
              onCommit: this.props.onCommit,
              definition: this.props.definition,
            });
          },
        },
      ]),
      t
    );
  })(a.PureComponent);
  function Qe(i) {
    return i.ctrlKey && i.key === "Enter";
  }
  function Ze(i) {
    return i !== "FragmentDefinition";
  }
  var Ke = (function (i) {
      R(t, i);
      function t() {
        var s, n, e, l;
        q(this, t);
        for (var c = arguments.length, f = Array(c), u = 0; u < c; u++)
          f[u] = arguments[u];
        return (
          (l =
            ((n =
              ((e = w(
                this,
                (s = t.__proto__ || Object.getPrototypeOf(t)).call.apply(
                  s,
                  [this].concat(f),
                ),
              )),
              e)),
            (e._handleChange = function (r) {
              e.props.setArgValue(r, !0);
            }),
            n)),
          w(e, l)
        );
      }
      return (
        P(t, [
          {
            key: "componentDidMount",
            value: function () {
              var n = this._ref,
                e = document.activeElement;
              n &&
                e &&
                !(e instanceof HTMLTextAreaElement) &&
                (n.focus(), n.setSelectionRange(0, n.value.length));
            },
          },
          {
            key: "render",
            value: function () {
              var n = this,
                e = this.props,
                l = e.arg,
                c = e.argValue,
                f = e.styleConfig,
                u = Q(l.type),
                r = typeof c.value == "string" ? c.value : "",
                o =
                  this.props.argValue.kind === "StringValue"
                    ? f.colors.string
                    : f.colors.number;
              return a.createElement(
                "span",
                { style: { color: o } },
                u.name === "String" ? '"' : "",
                a.createElement("input", {
                  style: {
                    border: "none",
                    borderBottom: "1px solid #888",
                    outline: "none",
                    width: Math.max(1, Math.min(15, r.length)) + "ch",
                    color: o,
                  },
                  ref: function (m) {
                    n._ref = m;
                  },
                  type: "text",
                  onChange: this._handleChange,
                  value: r,
                }),
                u.name === "String" ? '"' : "",
              );
            },
          },
        ]),
        t
      );
    })(a.PureComponent),
    Ee = (function (i) {
      R(t, i);
      function t() {
        var s, n, e, l;
        q(this, t);
        for (var c = arguments.length, f = Array(c), u = 0; u < c; u++)
          f[u] = arguments[u];
        return (
          (l =
            ((n =
              ((e = w(
                this,
                (s = t.__proto__ || Object.getPrototypeOf(t)).call.apply(
                  s,
                  [this].concat(f),
                ),
              )),
              e)),
            (e.state = { displayArgActions: !1 }),
            n)),
          w(e, l)
        );
      }
      return (
        P(t, [
          {
            key: "render",
            value: function () {
              var n = this,
                e = this.props,
                l = e.argValue,
                c = e.arg,
                f = e.styleConfig,
                u = Q(c.type),
                r = null;
              if (l) {
                if (l.kind === "Variable")
                  r = a.createElement(
                    "span",
                    { style: { color: f.colors.variable } },
                    "$",
                    l.name.value,
                  );
                else if ((0, v.isScalarType)(u))
                  u.name === "Boolean"
                    ? (r = a.createElement(
                        "select",
                        {
                          style: { color: f.colors.builtin },
                          onChange: this.props.setArgValue,
                          value: l.kind === "BooleanValue" ? l.value : void 0,
                        },
                        a.createElement(
                          "option",
                          { key: "true", value: "true" },
                          "true",
                        ),
                        a.createElement(
                          "option",
                          { key: "false", value: "false" },
                          "false",
                        ),
                      ))
                    : (r = a.createElement(Ke, {
                        setArgValue: this.props.setArgValue,
                        arg: c,
                        argValue: l,
                        onRunOperation: this.props.onRunOperation,
                        styleConfig: this.props.styleConfig,
                      }));
                else if ((0, v.isEnumType)(u))
                  l.kind === "EnumValue"
                    ? (r = a.createElement(
                        "select",
                        {
                          style: {
                            backgroundColor: "white",
                            color: f.colors.string2,
                          },
                          onChange: this.props.setArgValue,
                          value: l.value,
                        },
                        u.getValues().map(function (d) {
                          return a.createElement(
                            "option",
                            { key: d.name, value: d.name },
                            d.name,
                          );
                        }),
                      ))
                    : console.error(
                        "arg mismatch between arg and selection",
                        u,
                        l,
                      );
                else if ((0, v.isInputObjectType)(u))
                  if (l.kind === "ObjectValue") {
                    var o = u.getFields();
                    r = a.createElement(
                      "div",
                      { style: { marginLeft: 16 } },
                      Object.keys(o)
                        .sort()
                        .map(function (d) {
                          return a.createElement(Ge, {
                            key: d,
                            arg: o[d],
                            parentField: n.props.parentField,
                            selection: l,
                            modifyFields: n.props.setArgFields,
                            getDefaultScalarArgValue:
                              n.props.getDefaultScalarArgValue,
                            makeDefaultArg: n.props.makeDefaultArg,
                            onRunOperation: n.props.onRunOperation,
                            styleConfig: n.props.styleConfig,
                            onCommit: n.props.onCommit,
                            definition: n.props.definition,
                          });
                        }),
                    );
                  } else
                    console.error(
                      "arg mismatch between arg and selection",
                      u,
                      l,
                    );
              }
              var p = function () {
                  var b = c.name,
                    g = (n.props.definition.variableDefinitions || []).filter(
                      function (E) {
                        return E.variable.name.value.startsWith(b);
                      },
                    ).length,
                    C = void 0;
                  g > 0 ? (C = "" + b + g) : (C = b);
                  var _ = c.type.toString(),
                    A = (0, v.parseType)(_),
                    D = {
                      kind: "VariableDefinition",
                      variable: {
                        kind: "Variable",
                        name: { kind: "Name", value: C },
                      },
                      type: A,
                      directives: [],
                    },
                    B = function (x) {
                      return (
                        n.props.definition.variableDefinitions || []
                      ).find(function (T) {
                        return T.variable.name.value === x;
                      });
                    },
                    j = void 0,
                    G = {};
                  if (typeof l < "u" && l !== null) {
                    var U = (0, v.visit)(l, {
                        Variable: function (x) {
                          var T = x.name.value,
                            J = B(T);
                          if (((G[T] = G[T] + 1 || 1), !!J))
                            return J.defaultValue;
                        },
                      }),
                      K = D.type.kind === "NonNullType",
                      M = K ? k({}, D, { type: D.type.type }) : D;
                    j = k({}, M, { defaultValue: U });
                  } else j = D;
                  var $ = Object.entries(G)
                    .filter(function (E) {
                      var x = ye(E, 2);
                      x[0];
                      var T = x[1];
                      return T < 2;
                    })
                    .map(function (E) {
                      var x = ye(E, 2),
                        T = x[0];
                      return x[1], T;
                    });
                  if (j) {
                    var X = n.props.setArgValue(j, !1);
                    if (X) {
                      var ee = X.definitions.find(function (E) {
                          return E.operation &&
                            E.name &&
                            E.name.value &&
                            n.props.definition.name &&
                            n.props.definition.name.value
                            ? E.name.value === n.props.definition.name.value
                            : !1;
                        }),
                        y = []
                          .concat(I(ee.variableDefinitions || []), [j])
                          .filter(function (E) {
                            return $.indexOf(E.variable.name.value) === -1;
                          }),
                        S = k({}, ee, { variableDefinitions: y }),
                        O = X.definitions,
                        V = O.map(function (E) {
                          return ee === E ? S : E;
                        }),
                        L = k({}, X, { definitions: V });
                      n.props.onCommit(L);
                    }
                  }
                },
                m = function () {
                  if (!(!l || !l.name || !l.name.value)) {
                    var b = l.name.value,
                      g = (n.props.definition.variableDefinitions || []).find(
                        function (M) {
                          return M.variable.name.value === b;
                        },
                      );
                    if (g) {
                      var C = g.defaultValue,
                        _ = n.props.setArgValue(C, { commit: !1 });
                      if (_) {
                        var A = _.definitions.find(function (M) {
                          return M.name.value === n.props.definition.name.value;
                        });
                        if (!A) return;
                        var D = 0;
                        (0, v.visit)(A, {
                          Variable: function ($) {
                            $.name.value === b && (D = D + 1);
                          },
                        });
                        var B = A.variableDefinitions || [];
                        D < 2 &&
                          (B = B.filter(function (M) {
                            return M.variable.name.value !== b;
                          }));
                        var j = k({}, A, { variableDefinitions: B }),
                          G = _.definitions,
                          U = G.map(function (M) {
                            return A === M ? j : M;
                          }),
                          K = k({}, _, { definitions: U });
                        n.props.onCommit(K);
                      }
                    }
                  }
                },
                h = l && l.kind === "Variable",
                F = this.state.displayArgActions
                  ? a.createElement(
                      "button",
                      {
                        type: "submit",
                        className: "toolbar-button",
                        title: h
                          ? "Remove the variable"
                          : "Extract the current value into a GraphQL variable",
                        onClick: function (b) {
                          b.preventDefault(),
                            b.stopPropagation(),
                            h ? m() : p();
                        },
                        style: f.styles.actionButtonStyle,
                      },
                      a.createElement(
                        "span",
                        { style: { color: f.colors.variable } },
                        "$",
                      ),
                    )
                  : null;
              return a.createElement(
                "div",
                {
                  style: {
                    cursor: "pointer",
                    minHeight: "16px",
                    WebkitUserSelect: "none",
                    userSelect: "none",
                  },
                  "data-arg-name": c.name,
                  "data-arg-type": u.name,
                  className: "graphiql-explorer-" + c.name,
                },
                a.createElement(
                  "span",
                  {
                    style: { cursor: "pointer" },
                    onClick: function (b) {
                      var g = !l;
                      g ? n.props.addArg(!0) : n.props.removeArg(!0),
                        n.setState({ displayArgActions: g });
                    },
                  },
                  (0, v.isInputObjectType)(u)
                    ? a.createElement(
                        "span",
                        null,
                        l
                          ? this.props.styleConfig.arrowOpen
                          : this.props.styleConfig.arrowClosed,
                      )
                    : a.createElement(ae, {
                        checked: !!l,
                        styleConfig: this.props.styleConfig,
                      }),
                  a.createElement(
                    "span",
                    {
                      style: { color: f.colors.attribute },
                      title: c.description,
                      onMouseEnter: function () {
                        l !== null &&
                          typeof l < "u" &&
                          n.setState({ displayArgActions: !0 });
                      },
                      onMouseLeave: function () {
                        return n.setState({ displayArgActions: !1 });
                      },
                    },
                    c.name,
                    Se(c) ? "*" : "",
                    ": ",
                    F,
                    " ",
                  ),
                  " ",
                ),
                r || a.createElement("span", null),
                " ",
              );
            },
          },
        ]),
        t
      );
    })(a.PureComponent),
    Je = (function (i) {
      R(t, i);
      function t() {
        var s, n, e, l;
        q(this, t);
        for (var c = arguments.length, f = Array(c), u = 0; u < c; u++)
          f[u] = arguments[u];
        return (
          (l =
            ((n =
              ((e = w(
                this,
                (s = t.__proto__ || Object.getPrototypeOf(t)).call.apply(
                  s,
                  [this].concat(f),
                ),
              )),
              e)),
            (e._addFragment = function () {
              e.props.modifySelections(
                [].concat(I(e.props.selections), [
                  e._previousSelection || {
                    kind: "InlineFragment",
                    typeCondition: {
                      kind: "NamedType",
                      name: {
                        kind: "Name",
                        value: e.props.implementingType.name,
                      },
                    },
                    selectionSet: {
                      kind: "SelectionSet",
                      selections: e.props
                        .getDefaultFieldNames(e.props.implementingType)
                        .map(function (r) {
                          return {
                            kind: "Field",
                            name: { kind: "Name", value: r },
                          };
                        }),
                    },
                  },
                ]),
              );
            }),
            (e._removeFragment = function () {
              var r = e._getSelection();
              (e._previousSelection = r),
                e.props.modifySelections(
                  e.props.selections.filter(function (o) {
                    return o !== r;
                  }),
                );
            }),
            (e._getSelection = function () {
              var r = e.props.selections.find(function (o) {
                return (
                  o.kind === "InlineFragment" &&
                  o.typeCondition &&
                  e.props.implementingType.name === o.typeCondition.name.value
                );
              });
              if (!r) return null;
              if (r.kind === "InlineFragment") return r;
            }),
            (e._modifyChildSelections = function (r, o) {
              var p = e._getSelection();
              return e.props.modifySelections(
                e.props.selections.map(function (m) {
                  return m === p
                    ? {
                        directives: m.directives,
                        kind: "InlineFragment",
                        typeCondition: {
                          kind: "NamedType",
                          name: {
                            kind: "Name",
                            value: e.props.implementingType.name,
                          },
                        },
                        selectionSet: { kind: "SelectionSet", selections: r },
                      }
                    : m;
                }),
                o,
              );
            }),
            n)),
          w(e, l)
        );
      }
      return (
        P(t, [
          {
            key: "render",
            value: function () {
              var n = this,
                e = this.props,
                l = e.implementingType,
                c = e.schema,
                f = e.getDefaultFieldNames,
                u = e.styleConfig,
                r = this._getSelection(),
                o = l.getFields(),
                p = r ? (r.selectionSet ? r.selectionSet.selections : []) : [];
              return a.createElement(
                "div",
                { className: "graphiql-explorer-" + l.name },
                a.createElement(
                  "span",
                  {
                    style: { cursor: "pointer" },
                    onClick: r ? this._removeFragment : this._addFragment,
                  },
                  a.createElement(ae, {
                    checked: !!r,
                    styleConfig: this.props.styleConfig,
                  }),
                  a.createElement(
                    "span",
                    { style: { color: u.colors.atom } },
                    this.props.implementingType.name,
                  ),
                ),
                r
                  ? a.createElement(
                      "div",
                      { style: { marginLeft: 16 } },
                      Object.keys(o)
                        .sort()
                        .map(function (m) {
                          return a.createElement(Ae, {
                            key: m,
                            field: o[m],
                            selections: p,
                            modifySelections: n._modifyChildSelections,
                            schema: c,
                            getDefaultFieldNames: f,
                            getDefaultScalarArgValue:
                              n.props.getDefaultScalarArgValue,
                            makeDefaultArg: n.props.makeDefaultArg,
                            onRunOperation: n.props.onRunOperation,
                            onCommit: n.props.onCommit,
                            styleConfig: n.props.styleConfig,
                            definition: n.props.definition,
                            availableFragments: n.props.availableFragments,
                          });
                        }),
                    )
                  : null,
              );
            },
          },
        ]),
        t
      );
    })(a.PureComponent),
    Ye = (function (i) {
      R(t, i);
      function t() {
        var s, n, e, l;
        q(this, t);
        for (var c = arguments.length, f = Array(c), u = 0; u < c; u++)
          f[u] = arguments[u];
        return (
          (l =
            ((n =
              ((e = w(
                this,
                (s = t.__proto__ || Object.getPrototypeOf(t)).call.apply(
                  s,
                  [this].concat(f),
                ),
              )),
              e)),
            (e._addFragment = function () {
              e.props.modifySelections(
                [].concat(I(e.props.selections), [
                  e._previousSelection || {
                    kind: "FragmentSpread",
                    name: e.props.fragment.name,
                  },
                ]),
              );
            }),
            (e._removeFragment = function () {
              var r = e._getSelection();
              (e._previousSelection = r),
                e.props.modifySelections(
                  e.props.selections.filter(function (o) {
                    var p =
                      o.kind === "FragmentSpread" &&
                      o.name.value === e.props.fragment.name.value;
                    return !p;
                  }),
                );
            }),
            (e._getSelection = function () {
              var r = e.props.selections.find(function (o) {
                return (
                  o.kind === "FragmentSpread" &&
                  o.name.value === e.props.fragment.name.value
                );
              });
              return r;
            }),
            n)),
          w(e, l)
        );
      }
      return (
        P(t, [
          {
            key: "render",
            value: function () {
              var n = this.props.styleConfig,
                e = this._getSelection();
              return a.createElement(
                "div",
                {
                  className:
                    "graphiql-explorer-" + this.props.fragment.name.value,
                },
                a.createElement(
                  "span",
                  {
                    style: { cursor: "pointer" },
                    onClick: e ? this._removeFragment : this._addFragment,
                  },
                  a.createElement(ae, {
                    checked: !!e,
                    styleConfig: this.props.styleConfig,
                  }),
                  a.createElement(
                    "span",
                    {
                      style: { color: n.colors.def },
                      className:
                        "graphiql-explorer-" + this.props.fragment.name.value,
                    },
                    this.props.fragment.name.value,
                  ),
                ),
              );
            },
          },
        ]),
        t
      );
    })(a.PureComponent);
  function oe(i, t, s, n) {
    var e = [],
      l = !0,
      c = !1,
      f = void 0;
    try {
      for (
        var u = n[Symbol.iterator](), r;
        !(l = (r = u.next()).done);
        l = !0
      ) {
        var o = r.value;
        if ((0, v.isRequiredInputField)(o) || (t && t(s, o))) {
          var p = Q(o.type);
          (0, v.isInputObjectType)(p)
            ? (function () {
                var m = p.getFields();
                e.push({
                  kind: "ObjectField",
                  name: { kind: "Name", value: o.name },
                  value: {
                    kind: "ObjectValue",
                    fields: oe(
                      i,
                      t,
                      s,
                      Object.keys(m).map(function (h) {
                        return m[h];
                      }),
                    ),
                  },
                });
              })()
            : (0, v.isLeafType)(p) &&
              e.push({
                kind: "ObjectField",
                name: { kind: "Name", value: o.name },
                value: i(s, o, p),
              });
        }
      }
    } catch (m) {
      (c = !0), (f = m);
    } finally {
      try {
        !l && u.return && u.return();
      } finally {
        if (c) throw f;
      }
    }
    return e;
  }
  function _e(i, t, s) {
    var n = [],
      e = !0,
      l = !1,
      c = void 0;
    try {
      for (
        var f = s.args[Symbol.iterator](), u;
        !(e = (u = f.next()).done);
        e = !0
      ) {
        var r = u.value;
        if (Se(r) || (t && t(s, r))) {
          var o = Q(r.type);
          (0, v.isInputObjectType)(o)
            ? (function () {
                var p = o.getFields();
                n.push({
                  kind: "Argument",
                  name: { kind: "Name", value: r.name },
                  value: {
                    kind: "ObjectValue",
                    fields: oe(
                      i,
                      t,
                      s,
                      Object.keys(p).map(function (m) {
                        return p[m];
                      }),
                    ),
                  },
                });
              })()
            : (0, v.isLeafType)(o) &&
              n.push({
                kind: "Argument",
                name: { kind: "Name", value: r.name },
                value: i(s, r, o),
              });
        }
      }
    } catch (p) {
      (l = !0), (c = p);
    } finally {
      try {
        !e && f.return && f.return();
      } finally {
        if (l) throw c;
      }
    }
    return n;
  }
  var Ae = (function (i) {
    R(t, i);
    function t() {
      var s, n, e, l;
      q(this, t);
      for (var c = arguments.length, f = Array(c), u = 0; u < c; u++)
        f[u] = arguments[u];
      return (
        (l =
          ((n =
            ((e = w(
              this,
              (s = t.__proto__ || Object.getPrototypeOf(t)).call.apply(
                s,
                [this].concat(f),
              ),
            )),
            e)),
          (e.state = { displayFieldActions: !1 }),
          (e._addAllFieldsToSelections = function (r) {
            var o = r
                ? Object.keys(r).map(function (h) {
                    return {
                      kind: "Field",
                      name: { kind: "Name", value: h },
                      arguments: [],
                    };
                  })
                : [],
              p = { kind: "SelectionSet", selections: o },
              m = [].concat(
                I(
                  e.props.selections.filter(function (h) {
                    return h.kind === "InlineFragment"
                      ? !0
                      : h.name.value !== e.props.field.name;
                  }),
                ),
                [
                  {
                    kind: "Field",
                    name: { kind: "Name", value: e.props.field.name },
                    arguments: _e(
                      e.props.getDefaultScalarArgValue,
                      e.props.makeDefaultArg,
                      e.props.field,
                    ),
                    selectionSet: p,
                  },
                ],
              );
            e.props.modifySelections(m);
          }),
          (e._addFieldToSelections = function (r) {
            var o = [].concat(I(e.props.selections), [
              e._previousSelection || {
                kind: "Field",
                name: { kind: "Name", value: e.props.field.name },
                arguments: _e(
                  e.props.getDefaultScalarArgValue,
                  e.props.makeDefaultArg,
                  e.props.field,
                ),
              },
            ]);
            e.props.modifySelections(o);
          }),
          (e._handleUpdateSelections = function (r) {
            var o = e._getSelection();
            if (o && !r.altKey) e._removeFieldFromSelections();
            else {
              var p = (0, v.getNamedType)(e.props.field.type),
                m = (0, v.isObjectType)(p) && p.getFields(),
                h = !!m && r.altKey;
              h ? e._addAllFieldsToSelections(m) : e._addFieldToSelections(m);
            }
          }),
          (e._removeFieldFromSelections = function () {
            var r = e._getSelection();
            (e._previousSelection = r),
              e.props.modifySelections(
                e.props.selections.filter(function (o) {
                  return o !== r;
                }),
              );
          }),
          (e._getSelection = function () {
            var r = e.props.selections.find(function (o) {
              return o.kind === "Field" && e.props.field.name === o.name.value;
            });
            if (!r) return null;
            if (r.kind === "Field") return r;
          }),
          (e._setArguments = function (r, o) {
            var p = e._getSelection();
            if (!p) {
              console.error("Missing selection when setting arguments", r);
              return;
            }
            return e.props.modifySelections(
              e.props.selections.map(function (m) {
                return m === p
                  ? {
                      alias: p.alias,
                      arguments: r,
                      directives: p.directives,
                      kind: "Field",
                      name: p.name,
                      selectionSet: p.selectionSet,
                    }
                  : m;
              }),
              o,
            );
          }),
          (e._modifyChildSelections = function (r, o) {
            return e.props.modifySelections(
              e.props.selections.map(function (p) {
                if (p.kind === "Field" && e.props.field.name === p.name.value) {
                  if (p.kind !== "Field") throw new Error("invalid selection");
                  return {
                    alias: p.alias,
                    arguments: p.arguments,
                    directives: p.directives,
                    kind: "Field",
                    name: p.name,
                    selectionSet: { kind: "SelectionSet", selections: r },
                  };
                }
                return p;
              }),
              o,
            );
          }),
          n)),
        w(e, l)
      );
    }
    return (
      P(t, [
        {
          key: "render",
          value: function () {
            var n = this,
              e = this.props,
              l = e.field,
              c = e.schema,
              f = e.getDefaultFieldNames,
              u = e.styleConfig,
              r = this._getSelection(),
              o = ze(l.type),
              p = l.args.sort(function (g, C) {
                return g.name.localeCompare(C.name);
              }),
              m = "graphiql-explorer-node graphiql-explorer-" + l.name;
            l.isDeprecated && (m += " graphiql-explorer-deprecated");
            var h =
                (0, v.isObjectType)(o) ||
                (0, v.isInterfaceType)(o) ||
                (0, v.isUnionType)(o)
                  ? this.props.availableFragments &&
                    this.props.availableFragments[o.name]
                  : null,
              F = a.createElement(
                "div",
                { className: m },
                a.createElement(
                  "span",
                  {
                    title: l.description,
                    style: {
                      cursor: "pointer",
                      display: "inline-flex",
                      alignItems: "center",
                      minHeight: "16px",
                      WebkitUserSelect: "none",
                      userSelect: "none",
                    },
                    "data-field-name": l.name,
                    "data-field-type": o.name,
                    onClick: this._handleUpdateSelections,
                    onMouseEnter: function () {
                      var C =
                        (0, v.isObjectType)(o) &&
                        r &&
                        r.selectionSet &&
                        r.selectionSet.selections.filter(function (_) {
                          return _.kind !== "FragmentSpread";
                        }).length > 0;
                      C && n.setState({ displayFieldActions: !0 });
                    },
                    onMouseLeave: function () {
                      return n.setState({ displayFieldActions: !1 });
                    },
                  },
                  (0, v.isObjectType)(o)
                    ? a.createElement(
                        "span",
                        null,
                        r
                          ? this.props.styleConfig.arrowOpen
                          : this.props.styleConfig.arrowClosed,
                      )
                    : null,
                  (0, v.isObjectType)(o)
                    ? null
                    : a.createElement(ae, {
                        checked: !!r,
                        styleConfig: this.props.styleConfig,
                      }),
                  a.createElement(
                    "span",
                    {
                      style: { color: u.colors.property },
                      className: "graphiql-explorer-field-view",
                    },
                    l.name,
                  ),
                  this.state.displayFieldActions
                    ? a.createElement(
                        "button",
                        {
                          type: "submit",
                          className: "toolbar-button",
                          title:
                            "Extract selections into a new reusable fragment",
                          onClick: function (C) {
                            C.preventDefault(), C.stopPropagation();
                            var _ = o.name,
                              A = _ + "Fragment",
                              D = (h || []).filter(function (M) {
                                return M.name.value.startsWith(A);
                              }).length;
                            D > 0 && (A = "" + A + D);
                            var B = r
                                ? r.selectionSet
                                  ? r.selectionSet.selections
                                  : []
                                : [],
                              j = [
                                {
                                  kind: "FragmentSpread",
                                  name: { kind: "Name", value: A },
                                  directives: [],
                                },
                              ],
                              G = {
                                kind: "FragmentDefinition",
                                name: { kind: "Name", value: A },
                                typeCondition: {
                                  kind: "NamedType",
                                  name: { kind: "Name", value: o.name },
                                },
                                directives: [],
                                selectionSet: {
                                  kind: "SelectionSet",
                                  selections: B,
                                },
                              },
                              U = n._modifyChildSelections(j, !1);
                            if (U) {
                              var K = k({}, U, {
                                definitions: [].concat(I(U.definitions), [G]),
                              });
                              n.props.onCommit(K);
                            } else
                              console.warn(
                                "Unable to complete extractFragment operation",
                              );
                          },
                          style: k({}, u.styles.actionButtonStyle),
                        },
                        a.createElement("span", null, "…"),
                      )
                    : null,
                ),
                r && p.length
                  ? a.createElement(
                      "div",
                      {
                        style: { marginLeft: 16 },
                        className: "graphiql-explorer-graphql-arguments",
                      },
                      p.map(function (g) {
                        return a.createElement(We, {
                          key: g.name,
                          parentField: l,
                          arg: g,
                          selection: r,
                          modifyArguments: n._setArguments,
                          getDefaultScalarArgValue:
                            n.props.getDefaultScalarArgValue,
                          makeDefaultArg: n.props.makeDefaultArg,
                          onRunOperation: n.props.onRunOperation,
                          styleConfig: n.props.styleConfig,
                          onCommit: n.props.onCommit,
                          definition: n.props.definition,
                        });
                      }),
                    )
                  : null,
              );
            if (
              r &&
              ((0, v.isObjectType)(o) ||
                (0, v.isInterfaceType)(o) ||
                (0, v.isUnionType)(o))
            ) {
              var d = (0, v.isUnionType)(o) ? {} : o.getFields(),
                b = r ? (r.selectionSet ? r.selectionSet.selections : []) : [];
              return a.createElement(
                "div",
                { className: "graphiql-explorer-" + l.name },
                F,
                a.createElement(
                  "div",
                  { style: { marginLeft: 16 } },
                  h
                    ? h.map(function (g) {
                        var C = c.getType(g.typeCondition.name.value),
                          _ = g.name.value;
                        return C
                          ? a.createElement(Ye, {
                              key: _,
                              fragment: g,
                              selections: b,
                              modifySelections: n._modifyChildSelections,
                              schema: c,
                              styleConfig: n.props.styleConfig,
                              onCommit: n.props.onCommit,
                            })
                          : null;
                      })
                    : null,
                  Object.keys(d)
                    .sort()
                    .map(function (g) {
                      return a.createElement(t, {
                        key: g,
                        field: d[g],
                        selections: b,
                        modifySelections: n._modifyChildSelections,
                        schema: c,
                        getDefaultFieldNames: f,
                        getDefaultScalarArgValue:
                          n.props.getDefaultScalarArgValue,
                        makeDefaultArg: n.props.makeDefaultArg,
                        onRunOperation: n.props.onRunOperation,
                        styleConfig: n.props.styleConfig,
                        onCommit: n.props.onCommit,
                        definition: n.props.definition,
                        availableFragments: n.props.availableFragments,
                      });
                    }),
                  (0, v.isInterfaceType)(o) || (0, v.isUnionType)(o)
                    ? c.getPossibleTypes(o).map(function (g) {
                        return a.createElement(Je, {
                          key: g.name,
                          implementingType: g,
                          selections: b,
                          modifySelections: n._modifyChildSelections,
                          schema: c,
                          getDefaultFieldNames: f,
                          getDefaultScalarArgValue:
                            n.props.getDefaultScalarArgValue,
                          makeDefaultArg: n.props.makeDefaultArg,
                          onRunOperation: n.props.onRunOperation,
                          styleConfig: n.props.styleConfig,
                          onCommit: n.props.onCommit,
                          definition: n.props.definition,
                        });
                      })
                    : null,
                ),
              );
            }
            return F;
          },
        },
      ]),
      t
    );
  })(a.PureComponent);
  function Xe(i) {
    try {
      return i.trim() ? (0, v.parse)(i, { noLocation: !0 }) : null;
    } catch (t) {
      return new Error(t);
    }
  }
  var $e = {
      kind: "OperationDefinition",
      operation: "query",
      variableDefinitions: [],
      name: { kind: "Name", value: "MyQuery" },
      directives: [],
      selectionSet: { kind: "SelectionSet", selections: [] },
    },
    le = { kind: "Document", definitions: [$e] },
    Y = null;
  function et(i) {
    if (Y && Y[0] === i) return Y[1];
    var t = Xe(i);
    return t ? (t instanceof Error ? (Y ? Y[1] : le) : ((Y = [i, t]), t)) : le;
  }
  var Oe = {
      buttonStyle: {
        fontSize: "1.2em",
        padding: "0px",
        backgroundColor: "white",
        border: "none",
        margin: "5px 0px",
        height: "40px",
        width: "100%",
        display: "block",
        maxWidth: "none",
      },
      actionButtonStyle: {
        padding: "0px",
        backgroundColor: "white",
        border: "none",
        margin: "0px",
        maxWidth: "none",
        height: "15px",
        width: "15px",
        display: "inline-block",
        fontSize: "smaller",
      },
      explorerActionsStyle: {
        margin: "4px -8px -8px",
        paddingLeft: "8px",
        bottom: "0px",
        width: "100%",
        textAlign: "center",
        background: "none",
        borderTop: "none",
        borderBottom: "none",
      },
    },
    tt = (function (i) {
      R(t, i);
      function t() {
        var s, n, e, l;
        q(this, t);
        for (var c = arguments.length, f = Array(c), u = 0; u < c; u++)
          f[u] = arguments[u];
        return (
          (l =
            ((n =
              ((e = w(
                this,
                (s = t.__proto__ || Object.getPrototypeOf(t)).call.apply(
                  s,
                  [this].concat(f),
                ),
              )),
              e)),
            (e.state = { newOperationType: "query", displayTitleActions: !1 }),
            (e._modifySelections = function (r, o) {
              var p = e.props.definition;
              p.selectionSet.selections.length === 0 &&
                e._previousOperationDef &&
                (p = e._previousOperationDef);
              var m = void 0;
              if (p.kind === "FragmentDefinition")
                m = k({}, p, {
                  selectionSet: k({}, p.selectionSet, { selections: r }),
                });
              else if (p.kind === "OperationDefinition") {
                var h = r.filter(function (F) {
                  return !(F.kind === "Field" && F.name.value === "__typename");
                });
                h.length === 0 &&
                  (h = [
                    {
                      kind: "Field",
                      name: {
                        kind: "Name",
                        value: "__typename ## Placeholder value",
                      },
                    },
                  ]),
                  (m = k({}, p, {
                    selectionSet: k({}, p.selectionSet, { selections: h }),
                  }));
              }
              return e.props.onEdit(m, o);
            }),
            (e._onOperationRename = function (r) {
              return e.props.onOperationRename(r.target.value);
            }),
            (e._handlePotentialRun = function (r) {
              Qe(r) &&
                Ze(e.props.definition.kind) &&
                e.props.onRunOperation(e.props.name);
            }),
            (e._rootViewElId = function () {
              var r = e.props,
                o = r.operationType,
                p = r.name,
                m = o + "-" + (p || "unknown");
              return m;
            }),
            n)),
          w(e, l)
        );
      }
      return (
        P(t, [
          {
            key: "componentDidMount",
            value: function () {
              var n = this._rootViewElId();
              this.props.onMount(n);
            },
          },
          {
            key: "render",
            value: function () {
              var n = this,
                e = this.props,
                l = e.operationType,
                c = e.definition,
                f = e.schema,
                u = e.getDefaultFieldNames,
                r = e.styleConfig,
                o = this._rootViewElId(),
                p = this.props.fields || {},
                m = c,
                h = m.selectionSet.selections,
                F = this.props.name || se(l) + " Name";
              return a.createElement(
                "div",
                {
                  id: o,
                  tabIndex: "0",
                  onKeyDown: this._handlePotentialRun,
                  style: {
                    borderBottom: this.props.isLast
                      ? "none"
                      : "1px solid #d6d6d6",
                    marginBottom: "0em",
                    paddingBottom: "1em",
                  },
                },
                a.createElement(
                  "div",
                  {
                    style: { color: r.colors.keyword, paddingBottom: 4 },
                    className: "graphiql-operation-title-bar",
                    onMouseEnter: function () {
                      return n.setState({ displayTitleActions: !0 });
                    },
                    onMouseLeave: function () {
                      return n.setState({ displayTitleActions: !1 });
                    },
                  },
                  l,
                  " ",
                  a.createElement(
                    "span",
                    { style: { color: r.colors.def } },
                    a.createElement("input", {
                      style: {
                        color: r.colors.def,
                        border: "none",
                        borderBottom: "1px solid #888",
                        outline: "none",
                        width: Math.max(4, F.length) + "ch",
                      },
                      autoComplete: "false",
                      placeholder: se(l) + " Name",
                      value: this.props.name,
                      onKeyDown: this._handlePotentialRun,
                      onChange: this._onOperationRename,
                    }),
                  ),
                  this.props.onTypeName
                    ? a.createElement(
                        "span",
                        null,
                        a.createElement("br", null),
                        "on " + this.props.onTypeName,
                      )
                    : "",
                  this.state.displayTitleActions
                    ? a.createElement(
                        a.Fragment,
                        null,
                        a.createElement(
                          "button",
                          {
                            type: "submit",
                            className: "toolbar-button",
                            onClick: function () {
                              return n.props.onOperationDestroy();
                            },
                            style: k({}, r.styles.actionButtonStyle),
                          },
                          a.createElement("span", null, "✕"),
                        ),
                        a.createElement(
                          "button",
                          {
                            type: "submit",
                            className: "toolbar-button",
                            onClick: function () {
                              return n.props.onOperationClone();
                            },
                            style: k({}, r.styles.actionButtonStyle),
                          },
                          a.createElement("span", null, "⎘"),
                        ),
                      )
                    : "",
                ),
                Object.keys(p)
                  .sort()
                  .map(function (d) {
                    return a.createElement(Ae, {
                      key: d,
                      field: p[d],
                      selections: h,
                      modifySelections: n._modifySelections,
                      schema: f,
                      getDefaultFieldNames: u,
                      getDefaultScalarArgValue:
                        n.props.getDefaultScalarArgValue,
                      makeDefaultArg: n.props.makeDefaultArg,
                      onRunOperation: n.props.onRunOperation,
                      styleConfig: n.props.styleConfig,
                      onCommit: n.props.onCommit,
                      definition: n.props.definition,
                      availableFragments: n.props.availableFragments,
                    });
                  }),
              );
            },
          },
        ]),
        t
      );
    })(a.PureComponent);
  function nt() {
    return a.createElement(
      "div",
      {
        style: {
          fontFamily: "sans-serif",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          margin: "1em",
          marginTop: 0,
          flexGrow: 1,
          justifyContent: "flex-end",
        },
      },
      a.createElement(
        "div",
        {
          style: {
            borderTop: "1px solid #d6d6d6",
            paddingTop: "1em",
            width: "100%",
            textAlign: "center",
          },
        },
        "GraphiQL Explorer by ",
        a.createElement("a", { href: "https://www.onegraph.com" }, "OneGraph"),
      ),
      a.createElement(
        "div",
        null,
        "Contribute on",
        " ",
        a.createElement(
          "a",
          { href: "https://github.com/OneGraph/graphiql-explorer" },
          "GitHub",
        ),
      ),
    );
  }
  var we = (function (i) {
    R(t, i);
    function t() {
      var s, n, e, l;
      q(this, t);
      for (var c = arguments.length, f = Array(c), u = 0; u < c; u++)
        f[u] = arguments[u];
      return (
        (l =
          ((n =
            ((e = w(
              this,
              (s = t.__proto__ || Object.getPrototypeOf(t)).call.apply(
                s,
                [this].concat(f),
              ),
            )),
            e)),
          (e.state = {
            newOperationType: "query",
            operation: null,
            operationToScrollTo: null,
          }),
          (e._resetScroll = function () {
            var r = e._ref;
            r && (r.scrollLeft = 0);
          }),
          (e._onEdit = function (r) {
            return e.props.onEdit(r);
          }),
          (e._setAddOperationType = function (r) {
            e.setState({ newOperationType: r });
          }),
          (e._handleRootViewMount = function (r) {
            if (
              e.state.operationToScrollTo &&
              e.state.operationToScrollTo === r
            ) {
              var o = ".graphiql-explorer-root #" + r,
                p = document.querySelector(o);
              p && p.scrollIntoView();
            }
          }),
          n)),
        w(e, l)
      );
    }
    return (
      P(t, [
        {
          key: "componentDidMount",
          value: function () {
            this._resetScroll();
          },
        },
        {
          key: "render",
          value: function () {
            var n = this,
              e = this.props,
              l = e.schema,
              c = e.query,
              f = e.makeDefaultArg;
            if (!l)
              return a.createElement(
                "div",
                {
                  style: { fontFamily: "sans-serif" },
                  className: "error-container",
                },
                "No Schema Available",
              );
            var u = {
                colors: this.props.colors || qe,
                checkboxChecked: this.props.checkboxChecked || Ue,
                checkboxUnchecked: this.props.checkboxUnchecked || He,
                arrowClosed: this.props.arrowClosed || Be,
                arrowOpen: this.props.arrowOpen || Re,
                styles: this.props.styles ? k({}, Oe, this.props.styles) : Oe,
              },
              r = l.getQueryType(),
              o = l.getMutationType(),
              p = l.getSubscriptionType();
            if (!r && !o && !p)
              return a.createElement("div", null, "Missing query type");
            var m = r && r.getFields(),
              h = o && o.getFields(),
              F = p && p.getFields(),
              d = et(c),
              b = this.props.getDefaultFieldNames || be,
              g = this.props.getDefaultScalarArgValue || Ce,
              C = d.definitions,
              _ = C.map(function (y) {
                return y.kind === "FragmentDefinition" ||
                  y.kind === "OperationDefinition"
                  ? y
                  : null;
              }).filter(Boolean),
              A = _.length === 0 ? le.definitions : _,
              D = function (S, O) {
                var V =
                    O == null || O === ""
                      ? null
                      : { kind: "Name", value: O, loc: void 0 },
                  L = k({}, S, { name: V }),
                  E = d.definitions,
                  x = E.map(function (T) {
                    return S === T ? L : T;
                  });
                return k({}, d, { definitions: x });
              },
              B = function (S) {
                var O = void 0;
                S.kind === "FragmentDefinition"
                  ? (O = "fragment")
                  : (O = S.operation);
                var V = ((S.name && S.name.value) || "") + "Copy",
                  L = { kind: "Name", value: V, loc: void 0 },
                  E = k({}, S, { name: L }),
                  x = d.definitions,
                  T = [].concat(I(x), [E]);
                return (
                  n.setState({ operationToScrollTo: O + "-" + V }),
                  k({}, d, { definitions: T })
                );
              },
              j = function (S) {
                var O = d.definitions,
                  V = O.filter(function (L) {
                    return S !== L;
                  });
                return k({}, d, { definitions: V });
              },
              G = function (S) {
                var O = d.definitions,
                  V =
                    d.definitions.length === 1 &&
                    d.definitions[0] === le.definitions[0],
                  L = V
                    ? []
                    : O.filter(function (te) {
                        return te.kind === "OperationDefinition"
                          ? te.operation === S
                          : !1;
                      }),
                  E = "My" + se(S) + (L.length === 0 ? "" : L.length + 1),
                  x = "__typename # Placeholder value",
                  T = {
                    kind: "SelectionSet",
                    selections: [
                      {
                        kind: "Field",
                        name: { kind: "Name", value: x, loc: null },
                        arguments: [],
                        directives: [],
                        selectionSet: null,
                        loc: null,
                      },
                    ],
                    loc: null,
                  },
                  J = {
                    kind: "OperationDefinition",
                    operation: S,
                    name: { kind: "Name", value: E },
                    variableDefinitions: [],
                    directives: [],
                    selectionSet: T,
                    loc: null,
                  },
                  ce = V ? [J] : [].concat(I(d.definitions), [J]),
                  fe = k({}, d, { definitions: ce });
                n.setState({ operationToScrollTo: S + "-" + E }),
                  n.props.onEdit((0, v.print)(fe));
              },
              U = [
                m
                  ? a.createElement(
                      "option",
                      {
                        key: "query",
                        className: "toolbar-button",
                        style: u.styles.buttonStyle,
                        type: "link",
                        value: "query",
                      },
                      "Query",
                    )
                  : null,
                h
                  ? a.createElement(
                      "option",
                      {
                        key: "mutation",
                        className: "toolbar-button",
                        style: u.styles.buttonStyle,
                        type: "link",
                        value: "mutation",
                      },
                      "Mutation",
                    )
                  : null,
                F
                  ? a.createElement(
                      "option",
                      {
                        key: "subscription",
                        className: "toolbar-button",
                        style: u.styles.buttonStyle,
                        type: "link",
                        value: "subscription",
                      },
                      "Subscription",
                    )
                  : null,
              ].filter(Boolean),
              K =
                U.length === 0 || this.props.hideActions
                  ? null
                  : a.createElement(
                      "div",
                      {
                        style: {
                          minHeight: "50px",
                          maxHeight: "50px",
                          overflow: "none",
                        },
                      },
                      a.createElement(
                        "form",
                        {
                          className:
                            "variable-editor-title graphiql-explorer-actions",
                          style: k({}, u.styles.explorerActionsStyle, {
                            display: "flex",
                            flexDirection: "row",
                            alignItems: "center",
                            borderTop: "1px solid rgb(214, 214, 214)",
                          }),
                          onSubmit: function (S) {
                            return S.preventDefault();
                          },
                        },
                        a.createElement(
                          "span",
                          {
                            style: {
                              display: "inline-block",
                              flexGrow: "0",
                              textAlign: "right",
                            },
                          },
                          "Add new",
                          " ",
                        ),
                        a.createElement(
                          "select",
                          {
                            onChange: function (S) {
                              return n._setAddOperationType(S.target.value);
                            },
                            value: this.state.newOperationType,
                            style: { flexGrow: "2" },
                          },
                          U,
                        ),
                        a.createElement(
                          "button",
                          {
                            type: "submit",
                            className: "toolbar-button",
                            onClick: function () {
                              return n.state.newOperationType
                                ? G(n.state.newOperationType)
                                : null;
                            },
                            style: k({}, u.styles.buttonStyle, {
                              height: "22px",
                              width: "22px",
                            }),
                          },
                          a.createElement("span", null, "+"),
                        ),
                      ),
                    ),
              M =
                this.props.externalFragments &&
                this.props.externalFragments.reduce(function (y, S) {
                  if (S.kind === "FragmentDefinition") {
                    var O = S.typeCondition.name.value,
                      V = y[O] || [],
                      L = [].concat(I(V), [S]).sort(function (E, x) {
                        return E.name.value.localeCompare(x.name.value);
                      });
                    return k({}, y, he({}, O, L));
                  }
                  return y;
                }, {}),
              $ = A.reduce(function (y, S) {
                if (S.kind === "FragmentDefinition") {
                  var O = S.typeCondition.name.value,
                    V = y[O] || [],
                    L = [].concat(I(V), [S]).sort(function (E, x) {
                      return E.name.value.localeCompare(x.name.value);
                    });
                  return k({}, y, he({}, O, L));
                }
                return y;
              }, {}),
              X = k({}, $, M),
              ee = this.props.showAttribution
                ? a.createElement(nt, null)
                : null;
            return a.createElement(
              "div",
              {
                ref: function (S) {
                  n._ref = S;
                },
                style: {
                  fontSize: 12,
                  textOverflow: "ellipsis",
                  whiteSpace: "nowrap",
                  margin: 0,
                  padding: 8,
                  fontFamily:
                    'Consolas, Inconsolata, "Droid Sans Mono", Monaco, monospace',
                  display: "flex",
                  flexDirection: "column",
                  height: "100%",
                },
                className: "graphiql-explorer-root",
              },
              a.createElement(
                "div",
                { style: { flexGrow: "1", overflow: "scroll" } },
                A.map(function (y, S) {
                  var O = y && y.name && y.name.value,
                    V =
                      y.kind === "FragmentDefinition"
                        ? "fragment"
                        : (y && y.operation) || "query",
                    L = function (H) {
                      var Z = D(y, H);
                      n.props.onEdit((0, v.print)(Z));
                    },
                    E = function () {
                      var H = B(y);
                      n.props.onEdit((0, v.print)(H));
                    },
                    x = function () {
                      var H = j(y);
                      n.props.onEdit((0, v.print)(H));
                    },
                    T =
                      y.kind === "FragmentDefinition" &&
                      y.typeCondition.kind === "NamedType" &&
                      l.getType(y.typeCondition.name.value),
                    J = T instanceof v.GraphQLObjectType ? T.getFields() : null,
                    ce =
                      V === "query"
                        ? m
                        : V === "mutation"
                          ? h
                          : V === "subscription"
                            ? F
                            : y.kind === "FragmentDefinition"
                              ? J
                              : null,
                    fe =
                      y.kind === "FragmentDefinition"
                        ? y.typeCondition.name.value
                        : null,
                    te = function (H) {
                      var Z = (0, v.print)(H);
                      n.props.onEdit(Z);
                    };
                  return a.createElement(tt, {
                    key: S,
                    isLast: S === A.length - 1,
                    fields: ce,
                    operationType: V,
                    name: O,
                    definition: y,
                    onOperationRename: L,
                    onOperationDestroy: x,
                    onOperationClone: E,
                    onTypeName: fe,
                    onMount: n._handleRootViewMount,
                    onCommit: te,
                    onEdit: function (H, Z) {
                      var me = void 0;
                      if (
                        ((typeof Z > "u" ? "undefined" : je(Z)) === "object" &&
                        typeof Z.commit < "u"
                          ? (me = Z.commit)
                          : (me = !0),
                        H)
                      ) {
                        var de = k({}, d, {
                          definitions: d.definitions.map(function (Ve) {
                            return Ve === y ? H : Ve;
                          }),
                        });
                        return me && te(de), de;
                      } else return d;
                    },
                    schema: l,
                    getDefaultFieldNames: b,
                    getDefaultScalarArgValue: g,
                    makeDefaultArg: f,
                    onRunOperation: function () {
                      n.props.onRunOperation && n.props.onRunOperation(O);
                    },
                    styleConfig: u,
                    availableFragments: X,
                  });
                }),
                ee,
              ),
              K,
            );
          },
        },
      ]),
      t
    );
  })(a.PureComponent);
  we.defaultProps = { getDefaultFieldNames: be, getDefaultScalarArgValue: Ce };
  var rt = (function (i) {
      R(t, i);
      function t() {
        var s, n, e, l;
        q(this, t);
        for (var c = arguments.length, f = Array(c), u = 0; u < c; u++)
          f[u] = arguments[u];
        return (
          (l =
            ((n =
              ((e = w(
                this,
                (s = t.__proto__ || Object.getPrototypeOf(t)).call.apply(
                  s,
                  [this].concat(f),
                ),
              )),
              e)),
            (e.state = { hasError: !1, error: null, errorInfo: null }),
            n)),
          w(e, l)
        );
      }
      return (
        P(t, [
          {
            key: "componentDidCatch",
            value: function (n, e) {
              this.setState({ hasError: !0, error: n, errorInfo: e }),
                console.error("Error in component", n, e);
            },
          },
          {
            key: "render",
            value: function () {
              return this.state.hasError
                ? a.createElement(
                    "div",
                    { style: { padding: 18, fontFamily: "sans-serif" } },
                    a.createElement("div", null, "Something went wrong"),
                    a.createElement(
                      "details",
                      { style: { whiteSpace: "pre-wrap" } },
                      this.state.error ? this.state.error.toString() : null,
                      a.createElement("br", null),
                      this.state.errorInfo
                        ? this.state.errorInfo.componentStack
                        : null,
                    ),
                  )
                : this.props.children;
            },
          },
        ]),
        t
      );
    })(a.Component),
    pe = (function (i) {
      R(t, i);
      function t() {
        return (
          q(this, t),
          w(
            this,
            (t.__proto__ || Object.getPrototypeOf(t)).apply(this, arguments),
          )
        );
      }
      return (
        P(t, [
          {
            key: "render",
            value: function () {
              return a.createElement(
                "div",
                {
                  className: "docExplorerWrap",
                  style: {
                    height: "100%",
                    width: this.props.width,
                    minWidth: this.props.width,
                    zIndex: 7,
                    display: this.props.explorerIsOpen ? "flex" : "none",
                    flexDirection: "column",
                    overflow: "hidden",
                  },
                },
                a.createElement(
                  "div",
                  { className: "doc-explorer-title-bar" },
                  a.createElement(
                    "div",
                    { className: "doc-explorer-title" },
                    this.props.title,
                  ),
                  a.createElement(
                    "div",
                    { className: "doc-explorer-rhs" },
                    a.createElement(
                      "div",
                      {
                        className: "docExplorerHide",
                        onClick: this.props.onToggleExplorer,
                      },
                      "✕",
                    ),
                  ),
                ),
                a.createElement(
                  "div",
                  {
                    className: "doc-explorer-contents",
                    style: { padding: "0px", overflowY: "unset" },
                  },
                  a.createElement(rt, null, a.createElement(we, this.props)),
                ),
              );
            },
          },
        ]),
        t
      );
    })(a.PureComponent);
  (pe.defaultValue = ue),
    (pe.defaultProps = { width: 320, title: "Explorer" }),
    (ie.default = pe),
    Object.defineProperty(re, "__esModule", { value: !0 });
  var Fe = (re.Explorer = void 0),
    it = ie,
    xe = at(it);
  function at(i) {
    return i && i.__esModule ? i : { default: i };
  }
  (Fe = re.Explorer = xe.default), (re.default = xe.default);
  const dt = "",
    ot = {
      keyword: "hsl(var(--color-primary))",
      def: "hsl(var(--color-tertiary))",
      property: "hsl(var(--color-info))",
      qualifier: "hsl(var(--color-secondary))",
      attribute: "hsl(var(--color-tertiary))",
      number: "hsl(var(--color-success))",
      string: "hsl(var(--color-warning))",
      builtin: "hsl(var(--color-success))",
      string2: "hsl(var(--color-secondary))",
      variable: "hsl(var(--color-secondary))",
      atom: "hsl(var(--color-tertiary))",
    },
    lt = N.createElement(
      "svg",
      {
        viewBox: "0 -4 13 15",
        style: {
          color: "hsla(var(--color-neutral), var(--alpha-tertiary, 0.4))",
          marginRight: "var(--px-4)",
          height: "var(--px-16)",
          width: "var(--px-16)",
        },
      },
      N.createElement("path", {
        d: "M3.35355 6.85355L6.14645 9.64645C6.34171 9.84171 6.65829 9.84171 6.85355 9.64645L9.64645 6.85355C9.96143 6.53857 9.73835 6 9.29289 6L3.70711 6C3.26165 6 3.03857 6.53857 3.35355 6.85355Z",
        fill: "currentColor",
      }),
    ),
    st = N.createElement(
      "svg",
      {
        viewBox: "0 -2 13 15",
        style: {
          color: "hsla(var(--color-neutral), var(--alpha-tertiary, 0.4))",
          marginRight: "var(--px-4)",
          height: "var(--px-16)",
          width: "var(--px-16)",
        },
      },
      N.createElement("path", {
        d: "M6.35355 11.1464L9.14645 8.35355C9.34171 8.15829 9.34171 7.84171 9.14645 7.64645L6.35355 4.85355C6.03857 4.53857 5.5 4.76165 5.5 5.20711V10.7929C5.5 11.2383 6.03857 11.4614 6.35355 11.1464Z",
        fill: "currentColor",
      }),
    ),
    ut = N.createElement(
      "svg",
      {
        viewBox: "0 0 15 15",
        style: {
          color: "hsla(var(--color-neutral), var(--alpha-tertiary, 0.4))",
          marginRight: "var(--px-4)",
          height: "var(--px-16)",
          width: "var(--px-16)",
        },
      },
      N.createElement("circle", {
        cx: "7.5",
        cy: "7.5",
        r: "6",
        stroke: "currentColor",
        fill: "none",
      }),
    ),
    pt = N.createElement(
      "svg",
      {
        viewBox: "0 0 15 15",
        style: {
          color: "hsl(var(--color-info))",
          marginRight: "var(--px-4)",
          height: "var(--px-16)",
          width: "var(--px-16)",
        },
      },
      N.createElement("circle", {
        cx: "7.5",
        cy: "7.5",
        r: "7.5",
        fill: "currentColor",
      }),
      N.createElement("path", {
        d: "M4.64641 7.00106L6.8801 9.23256L10.5017 5.61325",
        fill: "none",
        stroke: "white",
        strokeWidth: "1.5",
      }),
    ),
    ct = {
      buttonStyle: {
        backgroundColor: "transparent",
        border: "none",
        color: "hsla(var(--color-neutral), var(--alpha-secondary, 0.6))",
        cursor: "pointer",
        fontSize: "1em",
      },
      explorerActionsStyle: { padding: "var(--px-8) var(--px-4)" },
      actionButtonStyle: {
        backgroundColor: "transparent",
        border: "none",
        color: "hsla(var(--color-neutral), var(--alpha-secondary, 0.6))",
        cursor: "pointer",
        fontSize: "1em",
      },
    };
  function ft(i) {
    const { setOperationName: t } = W.useEditorContext({ nonNull: !0 }),
      { schema: s } = W.useSchemaContext({ nonNull: !0 }),
      { run: n } = W.useExecutionContext({ nonNull: !0 }),
      e = N.useCallback(
        (f) => {
          f && t(f), n();
        },
        [n, t],
      ),
      [l, c] = W.useOperationsEditorState();
    return N.createElement(Fe, {
      schema: s,
      onRunOperation: e,
      explorerIsOpen: !0,
      colors: ot,
      arrowOpen: lt,
      arrowClosed: st,
      checkboxUnchecked: ut,
      checkboxChecked: pt,
      styles: ct,
      query: l,
      onEdit: c,
      ...i,
    });
  }
  function mt(i) {
    return {
      title: "GraphiQL Explorer",
      icon: () =>
        N.createElement(
          "svg",
          {
            height: "1em",
            strokeWidth: "1.5",
            viewBox: "0 0 24 24",
            fill: "none",
          },
          N.createElement("path", {
            d: "M18 6H20M22 6H20M20 6V4M20 6V8",
            stroke: "currentColor",
            strokeLinecap: "round",
            strokeLinejoin: "round",
          }),
          N.createElement("path", {
            d: "M21.4 20H2.6C2.26863 20 2 19.7314 2 19.4V11H21.4C21.7314 11 22 11.2686 22 11.6V19.4C22 19.7314 21.7314 20 21.4 20Z",
            stroke: "currentColor",
            strokeLinecap: "round",
            strokeLinejoin: "round",
          }),
          N.createElement("path", {
            d: "M2 11V4.6C2 4.26863 2.26863 4 2.6 4H8.77805C8.92127 4 9.05977 4.05124 9.16852 4.14445L12.3315 6.85555C12.4402 6.94876 12.5787 7 12.722 7H14",
            stroke: "currentColor",
            strokeLinecap: "round",
            strokeLinejoin: "round",
          }),
        ),
      content: () => N.createElement(ft, { ...i }),
    };
  }
  (z.explorerPlugin = mt),
    Object.defineProperty(z, Symbol.toStringTag, { value: "Module" });
});
