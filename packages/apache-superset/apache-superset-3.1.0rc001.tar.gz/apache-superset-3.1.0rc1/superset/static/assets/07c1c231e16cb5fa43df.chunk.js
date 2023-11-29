"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[8438],{27678:(e,t,n)=>{function a(e){var t=e.getBoundingClientRect(),n=document.documentElement;return{left:t.left+(window.pageXOffset||n.scrollLeft)-(n.clientLeft||document.body.clientLeft||0),top:t.top+(window.pageYOffset||n.scrollTop)-(n.clientTop||document.body.clientTop||0)}}n.d(t,{os:()=>a})},45598:(e,t,n)=>{var a=n(64836).default;Object.defineProperty(t,"__esModule",{value:!0}),t.default=function e(t){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},a=[];return l.default.Children.forEach(t,(function(t){(null!=t||n.keepEmpty)&&(Array.isArray(t)?a=a.concat(e(t)):(0,i.isFragment)(t)&&t.props?a=a.concat(e(t.props.children,n)):a.push(t))})),a};var l=a(n(67294)),i=n(59864)},97596:(e,t,n)=>{var a=n(64836).default;Object.defineProperty(t,"__esModule",{value:!0}),t.default=function(e,t,n,a){var i=l.default.unstable_batchedUpdates?function(e){l.default.unstable_batchedUpdates(n,e)}:n;return e.addEventListener&&e.addEventListener(t,i,a),{remove:function(){e.removeEventListener&&e.removeEventListener(t,i,a)}}};var l=a(n(90731))},54887:(e,t)=>{Object.defineProperty(t,"__esModule",{value:!0}),t.get=function(e,t){var r=arguments.length,o=i(e);return t=l[t]?"cssFloat"in e.style?"cssFloat":"styleFloat":t,1===r?o:function(e,t,l){if(t=t.toLowerCase(),"auto"===l){if("height"===t)return e.offsetHeight;if("width"===t)return e.offsetWidth}return t in a||(a[t]=n.test(t)),a[t]?parseFloat(l)||0:l}(e,t,o[t]||e.style[t])},t.getClientSize=function(){return{width:document.documentElement.clientWidth,height:window.innerHeight||document.documentElement.clientHeight}},t.getDocSize=function(){return{width:Math.max(document.documentElement.scrollWidth,document.body.scrollWidth),height:Math.max(document.documentElement.scrollHeight,document.body.scrollHeight)}},t.getOffset=function(e){var t=e.getBoundingClientRect(),n=document.documentElement;return{left:t.left+(window.pageXOffset||n.scrollLeft)-(n.clientLeft||document.body.clientLeft||0),top:t.top+(window.pageYOffset||n.scrollTop)-(n.clientTop||document.body.clientTop||0)}},t.getOuterHeight=function(e){return e===document.body?window.innerHeight||document.documentElement.clientHeight:e.offsetHeight},t.getOuterWidth=function(e){return e===document.body?document.documentElement.clientWidth:e.offsetWidth},t.getScroll=function(){return{scrollLeft:Math.max(document.documentElement.scrollLeft,document.body.scrollLeft),scrollTop:Math.max(document.documentElement.scrollTop,document.body.scrollTop)}},t.set=function e(t,a,r){var o=arguments.length;if(a=l[a]?"cssFloat"in t.style?"cssFloat":"styleFloat":a,3===o)return"number"==typeof r&&n.test(a)&&(r="".concat(r,"px")),t.style[a]=r,r;for(var s in a)a.hasOwnProperty(s)&&e(t,s,a[s]);return i(t)};var n=/margin|padding|width|height|max|min|offset/,a={left:!0,top:!0},l={cssFloat:1,styleFloat:1,float:1};function i(e){return 1===e.nodeType?e.ownerDocument.defaultView.getComputedStyle(e,null):{}}},55331:(e,t)=>{Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0,t.default=function(e){if(!e)return!1;if(e instanceof HTMLElement&&e.offsetParent)return!0;if(e instanceof SVGGraphicsElement&&e.getBBox){var t=e.getBBox(),n=t.width,a=t.height;if(n||a)return!0}if(e instanceof HTMLElement&&e.getBoundingClientRect){var l=e.getBoundingClientRect(),i=l.width,r=l.height;if(i||r)return!0}return!1}},8259:(e,t)=>{var n;function a(e){if("undefined"==typeof document)return 0;if(e||void 0===n){var t=document.createElement("div");t.style.width="100%",t.style.height="200px";var a=document.createElement("div"),l=a.style;l.position="absolute",l.top="0",l.left="0",l.pointerEvents="none",l.visibility="hidden",l.width="200px",l.height="150px",l.overflow="hidden",a.appendChild(t),document.body.appendChild(a);var i=t.offsetWidth;a.style.overflow="scroll";var r=t.offsetWidth;i===r&&(r=a.clientWidth),document.body.removeChild(a),n=i-r}return n}function l(e){var t=e.match(/^(.*)px$/),n=Number(null==t?void 0:t[1]);return Number.isNaN(n)?a():n}Object.defineProperty(t,"__esModule",{value:!0}),t.default=a,t.getTargetScrollBarSize=function(e){if(!("undefined"!=typeof document&&e&&e instanceof Element))return{width:0,height:0};var t=getComputedStyle(e,"::-webkit-scrollbar"),n=t.width,a=t.height;return{width:l(n),height:l(a)}}},18545:(e,t,n)=>{var a=n(75263).default;Object.defineProperty(t,"__esModule",{value:!0}),t.default=function(e){var t=l.useRef();return t.current=e,l.useCallback((function(){for(var e,n=arguments.length,a=new Array(n),l=0;l<n;l++)a[l]=arguments[l];return null===(e=t.current)||void 0===e?void 0:e.call.apply(e,[t].concat(a))}),[])};var l=a(n(67294))},82546:(e,t,n)=>{var a=n(64836).default,l=n(75263).default;Object.defineProperty(t,"__esModule",{value:!0}),t.useLayoutUpdateEffect=t.default=void 0;var i=l(n(67294)),r=(0,a(n(19158)).default)()?i.useLayoutEffect:i.useEffect,o=r;t.default=o,t.useLayoutUpdateEffect=function(e,t){var n=i.useRef(!0);r((function(){if(!n.current)return e()}),t),r((function(){return n.current=!1,function(){n.current=!0}}),[])}},60869:(e,t,n)=>{var a=n(75263).default,l=n(64836).default;Object.defineProperty(t,"__esModule",{value:!0}),t.default=function(e,t){var n=t||{},a=n.defaultValue,l=n.value,h=n.onChange,p=n.postState,g=(0,u.default)((function(){var t,n=void 0;return c(l)?(n=l,t=i.PROP):c(a)?(n="function"==typeof a?a():a,t=i.PROP):(n="function"==typeof e?e():e,t=i.INNER),[n,t,n]})),m=(0,r.default)(g,2),f=m[0],v=m[1],b=c(l)?l:f[0],y=p?p(b):b;(0,d.useLayoutUpdateEffect)((function(){v((function(e){var t=(0,r.default)(e,1)[0];return[l,i.PROP,t]}))}),[l]);var x=o.useRef(),Z=(0,s.default)((function(e,t){v((function(t){var n=(0,r.default)(t,3),a=n[0],l=n[1],o=n[2],s="function"==typeof e?e(a):e;if(s===a)return t;var d=l===i.INNER&&x.current!==o?o:a;return[s,i.INNER,d]}),t)})),w=(0,s.default)(h);return(0,d.default)((function(){var e=(0,r.default)(f,3),t=e[0],n=e[1],a=e[2];t!==a&&n===i.INNER&&(w(t,a),x.current=a)}),[f]),[y,Z]};var i,r=l(n(27424)),o=a(n(67294)),s=l(n(18545)),d=a(n(82546)),u=l(n(88558));function c(e){return void 0!==e}!function(e){e[e.INNER=0]="INNER",e[e.PROP=1]="PROP"}(i||(i={}))},88558:(e,t,n)=>{var a=n(75263).default,l=n(64836).default;Object.defineProperty(t,"__esModule",{value:!0}),t.default=function(e){var t=r.useRef(!1),n=r.useState(e),a=(0,i.default)(n,2),l=a[0],o=a[1];return r.useEffect((function(){return t.current=!1,function(){t.current=!0}}),[]),[l,function(e,n){n&&t.current||o(e)}]};var i=l(n(27424)),r=a(n(67294))},51794:(e,t,n)=>{n.d(t,{Z:()=>l});var a=n(67294);const l=(e,t)=>{var n,l;const[i,r]=(0,a.useState)(0),[o,s]=(0,a.useState)(!1),d=(0,a.useRef)({scrollWidth:0,parentElementWidth:0,plusRefWidth:0});return(0,a.useLayoutEffect)((()=>{var n;const a=e.current,l=null==t?void 0:t.current;if(!a)return;const{scrollWidth:i,clientWidth:o,childNodes:u}=a,c=d.current,h=(null==(n=a.parentElement)?void 0:n.clientWidth)||0,p=(null==l?void 0:l.offsetWidth)||0;if(d.current={scrollWidth:i,parentElementWidth:h,plusRefWidth:p},c.parentElementWidth!==h||c.scrollWidth!==i||c.plusRefWidth!==p)if(i>o){const e=6,t=(null==l?void 0:l.offsetWidth)||0,n=o-e,a=u.length;let i=0,d=0;for(let l=0;l<a;l+=1)n-e-i-t<=0&&(d+=1),i+=u[l].offsetWidth;a>1&&d?(s(!0),r(d)):(s(!1),r(1))}else s(!1),r(0)}),[null==(n=e.current)?void 0:n.offsetWidth,null==(l=e.current)?void 0:l.clientWidth,e]),[i,o]}},52564:(e,t,n)=>{n.d(t,{u:()=>Z});var a=n(73126),l=n(67294),i=n(11965),r=n(51995),o=n(61988),s=n(4715),d=n(58593),u=n(99612);const c=e=>i.iv`
  display: flex;
  font-size: ${e.typography.sizes.xl}px;
  font-weight: ${e.typography.weights.bold};
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

  & .dynamic-title,
  & .dynamic-title-input {
    display: inline-block;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  & .dynamic-title {
    cursor: default;
  }
  & .dynamic-title-input {
    border: none;
    padding: 0;
    outline: none;

    &::placeholder {
      color: ${e.colors.grayscale.light1};
    }
  }

  & .input-sizer {
    position: absolute;
    left: -9999px;
    display: inline-block;
  }
`,h=e=>{let{title:t,placeholder:n,onSave:a,canEdit:r,label:s}=e;const[h,p]=(0,l.useState)(!1),[g,m]=(0,l.useState)(t||""),f=(0,l.useRef)(null),[v,b]=(0,l.useState)(!1),{width:y,ref:x}=(0,u.NB)(),{width:Z,ref:w}=(0,u.NB)({refreshMode:"debounce"});(0,l.useEffect)((()=>{m(t)}),[t]),(0,l.useEffect)((()=>{if(h&&null!=f&&f.current&&(f.current.focus(),f.current.setSelectionRange)){const{length:e}=f.current.value;f.current.setSelectionRange(e,e),f.current.scrollLeft=f.current.scrollWidth}}),[h]),(0,l.useLayoutEffect)((()=>{null!=x&&x.current&&(x.current.innerHTML=(g||n).replace(/\s/g,"&nbsp;"))}),[g,n,x]),(0,l.useEffect)((()=>{f.current&&f.current.scrollWidth>f.current.clientWidth?b(!0):b(!1)}),[y,Z]);const $=(0,l.useCallback)((()=>{r&&!h&&p(!0)}),[r,h]),U=(0,l.useCallback)((()=>{if(!r)return;const e=g.trim();m(e),t!==e&&a(e),p(!1)}),[r,g,a,t]),_=(0,l.useCallback)((e=>{r&&h&&m(e.target.value)}),[r,h]),E=(0,l.useCallback)((e=>{var t;r&&"Enter"===e.key&&(e.preventDefault(),null==(t=f.current)||t.blur())}),[r]);return(0,i.tZ)("div",{css:c,ref:w},(0,i.tZ)(d.u,{id:"title-tooltip",title:v&&g&&!h?g:null},r?(0,i.tZ)("input",{className:"dynamic-title-input","aria-label":null!=s?s:(0,o.t)("Title"),ref:f,onChange:_,onBlur:U,onClick:$,onKeyPress:E,placeholder:n,value:g,css:i.iv`
              cursor: ${h?"text":"pointer"};

              ${y&&y>0&&i.iv`
                width: ${y+1}px;
              `}
            `}):(0,i.tZ)("span",{className:"dynamic-title","aria-label":null!=s?s:(0,o.t)("Title"),ref:f},g)),(0,i.tZ)("span",{ref:x,className:"input-sizer","aria-hidden":!0,tabIndex:-1}))};var p=n(79789),g=n(36674),m=n(70707),f=n(35932);const v=e=>i.iv`
  width: ${8*e.gridUnit}px;
  height: ${8*e.gridUnit}px;
  padding: 0;
  border: 1px solid ${e.colors.primary.dark2};

  &.ant-btn > span.anticon {
    line-height: 0;
    transition: inherit;
  }

  &:hover:not(:focus) > span.anticon {
    color: ${e.colors.primary.light1};
  }
`,b=e=>i.iv`
  display: flex;
  flex-direction: row;
  align-items: center;
  flex-wrap: nowrap;
  justify-content: space-between;
  background-color: ${e.colors.grayscale.light5};
  height: ${16*e.gridUnit}px;
  padding: 0 ${4*e.gridUnit}px;

  .editable-title {
    overflow: hidden;

    & > input[type='button'],
    & > span {
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
      white-space: nowrap;
    }
  }

  span[role='button'] {
    display: flex;
    height: 100%;
  }

  .title-panel {
    display: flex;
    align-items: center;
    min-width: 0;
    margin-right: ${12*e.gridUnit}px;
  }

  .right-button-panel {
    display: flex;
    align-items: center;
  }
`,y=e=>i.iv`
  display: flex;
  align-items: center;
  padding-left: ${2*e.gridUnit}px;

  & .fave-unfave-icon {
    padding: 0 ${e.gridUnit}px;

    &:first-of-type {
      padding-left: 0;
    }
  }
`,x=e=>i.iv`
  margin-left: ${2*e.gridUnit}px;
`,Z=e=>{let{editableTitleProps:t,showTitlePanelItems:n,certificatiedBadgeProps:l,showFaveStar:d,faveStarProps:u,titlePanelAdditionalItems:c,rightPanelAdditionalItems:Z,additionalActionsMenu:w,menuDropdownProps:$,showMenuDropdown:U=!0,tooltipProps:_}=e;const E=(0,r.Fg)();return(0,i.tZ)("div",{css:b,className:"header-with-actions"},(0,i.tZ)("div",{className:"title-panel"},(0,i.tZ)(h,t),n&&(0,i.tZ)("div",{css:y},(null==l?void 0:l.certifiedBy)&&(0,i.tZ)(p.Z,l),d&&(0,i.tZ)(g.Z,u),c)),(0,i.tZ)("div",{className:"right-button-panel"},Z,(0,i.tZ)("div",{css:x},U&&(0,i.tZ)(s.Gj,(0,a.Z)({trigger:["click"],overlay:w},$),(0,i.tZ)(f.Z,{css:v,buttonStyle:"tertiary","aria-label":(0,o.t)("Menu actions trigger"),tooltip:null==_?void 0:_.text,placement:null==_?void 0:_.placement},(0,i.tZ)(m.Z.MoreHoriz,{iconColor:E.colors.primary.dark2,iconSize:"l"}))))))}},80663:(e,t,n)=>{n.d(t,{Z:()=>d});var a=n(67294),l=n(29119),i=n(51995),r=n(61337),o=n(11965);const s=i.iK.div`
  position: absolute;
  height: 100%;

  :hover .sidebar-resizer::after {
    background-color: ${e=>{let{theme:t}=e;return t.colors.primary.base}};
  }

  .sidebar-resizer {
    // @z-index-above-sticky-header (100) + 1 = 101
    z-index: 101;
  }

  .sidebar-resizer::after {
    display: block;
    content: '';
    width: 1px;
    height: 100%;
    margin: 0 auto;
  }
`,d=e=>{let{id:t,initialWidth:n,minWidth:i,maxWidth:d,enable:u,children:c}=e;const[h,p]=function(e,t){const n=(0,a.useRef)(),[l,i]=(0,a.useState)(t);return(0,a.useEffect)((()=>{var t;n.current=null!=(t=n.current)?t:(0,r.rV)(r.dR.common__resizable_sidebar_widths,{}),n.current[e]&&i(n.current[e])}),[e]),[l,function(t){i(t),(0,r.LS)(r.dR.common__resizable_sidebar_widths,{...n.current,[e]:t})}]}(t,n);return(0,o.tZ)(a.Fragment,null,(0,o.tZ)(s,null,(0,o.tZ)(l.e,{enable:{right:u},handleClasses:{right:"sidebar-resizer"},size:{width:h,height:"100%"},minWidth:i,maxWidth:d,onResizeStop:(e,t,n,a)=>p(h+a.width)})),c(h))}},12685:(e,t,n)=>{n.r(t),n.d(t,{datasetReducer:()=>ut,default:()=>ht});var a=n(67294),l=n(16550),i=n(31069),r=n(61988),o=n(68492),s=n(15926),d=n.n(s),u=n(72570);const c=(e,t)=>{const[n,l]=(0,a.useState)([]),s=t?encodeURIComponent(t):void 0,c=(0,a.useCallback)((async e=>{let t,n=[],a=0;for(;void 0===t||n.length<t;){const l=d().encode_uri({filters:e,page:a});try{const e=await i.Z.get({endpoint:`/api/v1/dataset/?q=${l}`});({count:t}=e.json);const{json:{result:r}}=e;n=[...n,...r],a+=1}catch(e){(0,u.Gb)((0,r.t)("There was an error fetching dataset")),o.Z.error((0,r.t)("There was an error fetching dataset"),e)}}l(n)}),[]);(0,a.useEffect)((()=>{const n=[{col:"database",opr:"rel_o_m",value:null==e?void 0:e.id},{col:"schema",opr:"eq",value:s},{col:"sql",opr:"dataset_is_null_or_empty",value:!0}];t&&c(n)}),[null==e?void 0:e.id,t,s,c]);const h=(0,a.useMemo)((()=>null==n?void 0:n.map((e=>e.table_name))),[n]);return{datasets:n,datasetNames:h}};var h,p=n(52564),g=n(35932),m=n(70707),f=n(83862);!function(e){e[e.selectDatabase=0]="selectDatabase",e[e.selectSchema=1]="selectSchema",e[e.selectTable=2]="selectTable",e[e.changeDataset=3]="changeDataset"}(h||(h={}));var v=n(51995),b=n(11965);const y=v.iK.div`
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  background-color: ${e=>{let{theme:t}=e;return t.colors.grayscale.light5}};
`,x=v.iK.div`
  width: ${e=>{let{theme:t,width:n}=e;return null!=n?n:80*t.gridUnit}}px;
  max-width: ${e=>{let{theme:t,width:n}=e;return null!=n?n:80*t.gridUnit}}px;
  flex-direction: column;
  flex: 1 0 auto;
`,Z=v.iK.div`
  display: flex;
  flex-direction: column;
  flex-grow: 1;
`,w=v.iK.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
`,$=(0,v.iK)(w)`
  flex: 1 0 auto;
  position: relative;
`,U=(0,v.iK)(w)`
  flex: 1 0 auto;
  height: auto;
`,_=(0,v.iK)(w)`
  flex: 0 0 auto;
  height: ${e=>{let{theme:t}=e;return 16*t.gridUnit}}px;
  z-index: 0;
`,E=v.iK.div`
  ${e=>{let{theme:t}=e;return`\n  flex: 0 0 auto;\n  height: ${16*t.gridUnit}px;\n  border-bottom: 2px solid ${t.colors.grayscale.light2};\n\n  .header-with-actions {\n    height: ${15.5*t.gridUnit}px;\n  }\n  `}}
`,T=v.iK.div`
  ${e=>{let{theme:t}=e;return`\n  margin: ${4*t.gridUnit}px;\n  font-size: ${t.typography.sizes.xl}px;\n  font-weight: ${t.typography.weights.bold};\n  `}}
`,S=v.iK.div`
  ${e=>{let{theme:t}=e;return`\n  height: 100%;\n  border-right: 1px solid ${t.colors.grayscale.light2};\n  `}}
`,C=v.iK.div`
  width: 100%;
  position: relative;
`,P=v.iK.div`
  ${e=>{let{theme:t}=e;return`\n  border-left: 1px solid ${t.colors.grayscale.light2};\n  color: ${t.colors.success.base};\n  `}}
`,k=v.iK.div`
  ${e=>{let{theme:t}=e;return`\n  height: ${16*t.gridUnit}px;\n  width: 100%;\n  border-top: 1px solid ${t.colors.grayscale.light2};\n  border-bottom: 1px solid ${t.colors.grayscale.light2};\n  color: ${t.colors.info.base};\n  border-top: ${t.gridUnit/4}px solid\n    ${t.colors.grayscale.light2};\n  padding: ${4*t.gridUnit}px;\n  display: flex;\n  justify-content: flex-end;\n  background-color: ${t.colors.grayscale.light5};\n  z-index: ${t.zIndex.max}\n  `}}
`,I=v.iK.div`
  .ant-btn {
    span {
      margin-right: 0;
    }

    &:disabled {
      svg {
        color: ${e=>{let{theme:t}=e;return t.colors.grayscale.light1}};
      }
    }
  }
`,M=e=>b.iv`
  width: ${21.5*e.gridUnit}px;

  &:disabled {
    background-color: ${e.colors.grayscale.light3};
    color: ${e.colors.grayscale.light1};
  }
`,R=(0,r.t)("New dataset"),N={text:(0,r.t)("Select a database table and create dataset"),placement:"bottomRight"},L=()=>(0,b.tZ)(g.Z,{buttonStyle:"primary",tooltip:null==N?void 0:N.text,placement:null==N?void 0:N.placement,disabled:!0,css:M},(0,b.tZ)(m.Z.Save,{iconSize:"m"}),(0,r.t)("Save")),z=()=>(0,b.tZ)(f.Menu,null,(0,b.tZ)(f.Menu.Item,null,(0,r.t)("Settings")),(0,b.tZ)(f.Menu.Item,null,(0,r.t)("Delete")));function O(e){let{setDataset:t,title:n=R,editing:l=!1}=e;const i={title:null!=n?n:R,placeholder:R,onSave:e=>{t({type:h.changeDataset,payload:{name:"dataset_name",value:e}})},canEdit:!1,label:(0,r.t)("dataset name")};return(0,b.tZ)(I,null,l?(0,b.tZ)(p.u,{editableTitleProps:i,showTitlePanelItems:!1,showFaveStar:!1,faveStarProps:{itemId:1,saveFaveStar:()=>{}},titlePanelAdditionalItems:(0,b.tZ)(a.Fragment,null),rightPanelAdditionalItems:L(),additionalActionsMenu:z(),menuDropdownProps:{disabled:!0},tooltipProps:N}):(0,b.tZ)(T,null,n||R))}var K,W,D=n(82607),V=n(71262),F=n(73126),j=n(73727),A=n(55786),H=n(93197),B=n(94301);function q(){return q=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var a in n)Object.prototype.hasOwnProperty.call(n,a)&&(e[a]=n[a])}return e},q.apply(this,arguments)}const X=(e,t)=>{let{title:n,titleId:l,...i}=e;return a.createElement("svg",q({xmlns:"http://www.w3.org/2000/svg",width:160,height:166,fill:"none",ref:t,"aria-labelledby":l},i),n?a.createElement("title",{id:l},n):null,K||(K=a.createElement("path",{fill:"#FAFAFA",fillRule:"evenodd",d:"M123.638 8a.5.5 0 0 0-.5.5V158h28.758V8.5a.5.5 0 0 0-.5-.5h-27.758ZM84.793 40.643a.5.5 0 0 1 .5-.5h27.759a.5.5 0 0 1 .5.5V158H84.793V40.643ZM46.95 72.285a.5.5 0 0 0-.5.5V158h28.758V72.785a.5.5 0 0 0-.5-.5H46.95ZM8.604 93.715a.5.5 0 0 0-.5.5V158h28.758V94.215a.5.5 0 0 0-.5-.5H8.604Z",clipRule:"evenodd"})),W||(W=a.createElement("path",{fill:"#D9D9D9",d:"M123.138 158h-.5v.5h.5v-.5Zm28.758 0v.5h.5v-.5h-.5Zm-38.344 0v.5h.5v-.5h-.5Zm-28.759 0h-.5v.5h.5v-.5Zm-38.344-.001h-.5v.5h.5v-.5Zm28.758 0v.5h.5v-.5h-.5ZM8.104 158h-.5v.5h.5v-.5Zm28.758 0v.5h.5v-.5h-.5ZM123.638 8.5v-1a1 1 0 0 0-1 1h1Zm0 149.5V8.5h-1V158h1Zm28.258-.5h-28.758v1h28.758v-1Zm-.5-149V158h1V8.5h-1Zm0 0h1a1 1 0 0 0-1-1v1Zm-27.758 0h27.758v-1h-27.758v1ZM85.293 39.643a1 1 0 0 0-1 1h1v-1Zm27.759 0H85.293v1h27.759v-1Zm1 1a1 1 0 0 0-1-1v1h1Zm0 117.357V40.643h-1V158h1Zm-29.259.5h28.759v-1H84.793v1Zm-.5-117.857V158h1V40.643h-1ZM46.95 72.785v-1a1 1 0 0 0-1 1h1Zm0 85.214V72.785h-1V158h1Zm28.258-.5H46.45v1h28.758v-1Zm-.5-84.714V158h1V72.785h-1Zm0 0h1a1 1 0 0 0-1-1v1Zm-27.758 0h27.758v-1H46.95v1ZM8.604 94.215v-1a1 1 0 0 0-1 1h1Zm0 63.785V94.215h-1V158h1Zm28.258-.5H8.104v1h28.758v-1Zm-.5-63.285V158h1V94.215h-1Zm0 0h1a1 1 0 0 0-1-1v1Zm-27.758 0h27.758v-1H8.604v1Z"})))},G=(0,a.forwardRef)(X);var Y=n(14114),Q=n(34858),J=n(93139),ee=n(30381),te=n.n(ee),ne=n(51794),ae=n(58593);const le=v.iK.div`
  & > span {
    width: 100%;
    display: flex;

    .ant-tooltip-open {
      display: inline;
    }
  }
`,ie=v.iK.span`
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: inline-block;
  width: 100%;
  vertical-align: bottom;
`,re=v.iK.span`
  &:not(:last-child)::after {
    content: ', ';
  }
`,oe=v.iK.div`
  .link {
    color: ${e=>{let{theme:t}=e;return t.colors.grayscale.light5}};
    display: block;
    text-decoration: underline;
  }
`,se=v.iK.span`
  ${e=>{let{theme:t}=e;return`\n  cursor: pointer;\n  color: ${t.colors.primary.dark1};\n  font-weight: ${t.typography.weights.normal};\n  `}}
`;function de(e){let{items:t,renderVisibleItem:n=(e=>e),renderTooltipItem:l=(e=>e),getKey:i=(e=>e),maxLinks:o=20}=e;const s=(0,a.useRef)(null),d=(0,a.useRef)(null),[u,c]=(0,ne.Z)(s,d),h=(0,a.useMemo)((()=>t.length>o?t.length-o:void 0),[t,o]),p=(0,a.useMemo)((()=>(0,b.tZ)(ie,{ref:s},t.map((e=>(0,b.tZ)(re,{key:i(e)},n(e)))))),[i,t,n]),g=(0,a.useMemo)((()=>t.slice(0,o).map((e=>(0,b.tZ)(oe,{key:i(e)},l(e))))),[i,t,o,l]);return(0,b.tZ)(le,null,(0,b.tZ)(ae.u,{placement:"top",title:u?(0,b.tZ)(a.Fragment,null,g,h&&(0,b.tZ)("span",null,(0,r.t)("+ %s more",h))):null},p,c&&(0,b.tZ)(se,{ref:d},"+",u)))}const ue=e=>({key:e.id,to:`/superset/dashboard/${e.id}`,target:"_blank",rel:"noreferer noopener",children:e.dashboard_title}),ce=e=>b.iv`
  color: ${e.colors.grayscale.light5};
  text-decoration: underline;
  &:hover {
    color: inherit;
  }
`,he=[{key:"slice_name",title:(0,r.t)("Chart"),width:"320px",sorter:!0,render:(e,t)=>(0,b.tZ)(j.rU,{to:t.url},t.slice_name)},{key:"owners",title:(0,r.t)("Chart owners"),width:"242px",render:(e,t)=>{var n,a;return(0,b.tZ)(de,{items:null!=(n=null==(a=t.owners)?void 0:a.map((e=>`${e.first_name} ${e.last_name}`)))?n:[]})}},{key:"last_saved_at",title:(0,r.t)("Chart last modified"),width:"209px",sorter:!0,defaultSortOrder:"descend",render:(e,t)=>t.last_saved_at?te().utc(t.last_saved_at).fromNow():null},{key:"last_saved_by.first_name",title:(0,r.t)("Chart last modified by"),width:"216px",sorter:!0,render:(e,t)=>t.last_saved_by?`${t.last_saved_by.first_name} ${t.last_saved_by.last_name}`:null},{key:"dashboards",title:(0,r.t)("Dashboard usage"),width:"420px",render:(e,t)=>(0,b.tZ)(de,{items:t.dashboards,renderVisibleItem:e=>(0,b.tZ)(j.rU,ue(e)),renderTooltipItem:e=>(0,b.tZ)(j.rU,(0,F.Z)({},ue(e),{css:ce})),getKey:e=>e.id})}],pe=e=>b.iv`
  && th.ant-table-cell {
    color: ${e.colors.grayscale.light1};
  }

  .ant-table-placeholder {
    display: none;
  }
`,ge=(0,b.tZ)(a.Fragment,null,(0,b.tZ)(m.Z.PlusOutlined,{iconSize:"m",css:b.iv`
        & > .anticon {
          line-height: 0;
        }
      `}),(0,r.t)("Create chart with dataset")),me=(0,v.iK)(B.XJ)`
  margin: ${e=>{let{theme:t}=e;return 13*t.gridUnit}}px 0;
`,fe=e=>{let{datasetId:t}=e;const{loading:n,recordCount:l,data:i,onChange:o}=(e=>{const{addDangerToast:t}=(0,Y.e1)(),n=(0,a.useMemo)((()=>[{id:"datasource_id",operator:J.p.equals,value:e}]),[e]),{state:{loading:l,resourceCount:i,resourceCollection:o},fetchData:s}=(0,Q.Yi)("chart",(0,r.t)("chart"),t,!0,[],n),d=(0,a.useMemo)((()=>o.map((e=>({...e,key:e.id})))),[o]),u=(0,a.useCallback)(((e,t,n)=>{var a,l;const i=(null!=(a=e.current)?a:1)-1,r=null!=(l=e.pageSize)?l:0,o=(0,A.Z)(n).filter((e=>{let{columnKey:t}=e;return"string"==typeof t})).map((e=>{let{columnKey:t,order:n}=e;return{id:t,desc:"descend"===n}}));s({pageIndex:i,pageSize:r,sortBy:o,filters:[]})}),[s]);return(0,a.useEffect)((()=>{s({pageIndex:0,pageSize:25,sortBy:[{id:"last_saved_at",desc:!0}],filters:[]})}),[s]),{loading:l,recordCount:i,data:d,onChange:u}})(t),s=(0,a.useCallback)((()=>window.open(`/explore/?dataset_type=table&dataset_id=${t}`,"_blank")),[t]);return(0,b.tZ)("div",{css:i.length?null:pe},(0,b.tZ)(H.ZP,{columns:he,data:i,size:H.ex.MIDDLE,defaultPageSize:25,recordCount:l,loading:n,onChange:o}),i.length||n?null:(0,b.tZ)(me,{image:(0,b.tZ)(G,null),title:(0,r.t)("No charts"),description:(0,r.t)("This dataset is not used to power any charts."),buttonText:ge,buttonAction:s}))},ve=(0,v.iK)(V.ZP)`
  ${e=>{let{theme:t}=e;return`\n  margin-top: ${8.5*t.gridUnit}px;\n  padding-left: ${4*t.gridUnit}px;\n  padding-right: ${4*t.gridUnit}px;\n\n  .ant-tabs-top > .ant-tabs-nav::before {\n    width: ${50*t.gridUnit}px;\n  }\n  `}}
`,be=v.iK.div`
  ${e=>{let{theme:t}=e;return`\n  .ant-badge {\n    width: ${8*t.gridUnit}px;\n    margin-left: ${2.5*t.gridUnit}px;\n  }\n  `}}
`,ye={USAGE_TEXT:(0,r.t)("Usage"),COLUMNS_TEXT:(0,r.t)("Columns"),METRICS_TEXT:(0,r.t)("Metrics")},xe=e=>{let{id:t}=e;const{usageCount:n}=(e=>{const[t,n]=(0,a.useState)(0),l=(0,a.useCallback)((()=>i.Z.get({endpoint:`/api/v1/dataset/${e}/related_objects`}).then((e=>{let{json:t}=e;n(null==t?void 0:t.charts.count)})).catch((e=>{(0,u.Gb)((0,r.t)("There was an error fetching dataset's related objects")),o.Z.error(e)}))),[e]);return(0,a.useEffect)((()=>{e&&l()}),[e,l]),{usageCount:t}})(t),l=(0,b.tZ)(be,null,(0,b.tZ)("span",null,ye.USAGE_TEXT),n>0&&(0,b.tZ)(D.Z,{count:n}));return(0,b.tZ)(ve,{moreIcon:null,fullWidth:!1},(0,b.tZ)(V.ZP.TabPane,{tab:ye.COLUMNS_TEXT,key:"1"}),(0,b.tZ)(V.ZP.TabPane,{tab:ye.METRICS_TEXT,key:"2"}),(0,b.tZ)(V.ZP.TabPane,{tab:l,key:"3"},(0,b.tZ)(fe,{datasetId:t})))};var Ze=n(29487);const we=(e,t,n)=>{var a;return null==t||null==(a=t[e])||null==a.localeCompare?void 0:a.localeCompare(null==n?void 0:n[e])};var $e=n(89419);const Ue=v.iK.div`
  padding: ${e=>{let{theme:t}=e;return 8*t.gridUnit}}px
    ${e=>{let{theme:t}=e;return 6*t.gridUnit}}px;

  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
`,_e=(0,v.iK)(B.XJ)`
  max-width: 50%;

  p {
    width: ${e=>{let{theme:t}=e;return 115*t.gridUnit}}px;
  }
`,Ee=(0,r.t)("Datasets can be created from database tables or SQL queries. Select a database table to the left or "),Te=(0,r.t)("create dataset from SQL query"),Se=(0,r.t)(" to open SQL Lab. From there you can save the query as a dataset."),Ce=(0,r.t)("Select dataset source"),Pe=(0,r.t)("No table columns"),ke=(0,r.t)("This database table does not contain any data. Please select a different table."),Ie=(0,r.t)("An Error Occurred"),Me=(0,r.t)("Unable to load columns for the selected table. Please select a different table."),Re=e=>{const{hasError:t,tableName:n,hasColumns:l}=e;let i="empty-dataset.svg",r=Ce,o=(0,b.tZ)(a.Fragment,null,Ee,(0,b.tZ)(j.rU,{to:"/sqllab"},(0,b.tZ)("span",{role:"button",tabIndex:0},Te)),Se);return t?(r=Ie,o=(0,b.tZ)(a.Fragment,null,Me),i=void 0):n&&!l&&(i="no-columns.svg",r=Pe,o=(0,b.tZ)(a.Fragment,null,ke)),(0,b.tZ)(Ue,null,(0,b.tZ)(_e,{image:i,title:r,description:o}))};var Ne;!function(e){e.ABSOLUTE="absolute",e.RELATIVE="relative"}(Ne||(Ne={}));const Le=v.iK.div`
  ${e=>{let{theme:t,position:n}=e;return`\n  position: ${n};\n  margin: ${4*t.gridUnit}px\n    ${3*t.gridUnit}px\n    ${3*t.gridUnit}px\n    ${6*t.gridUnit}px;\n  font-size: ${6*t.gridUnit}px;\n  font-weight: ${t.typography.weights.medium};\n  padding-bottom: ${3*t.gridUnit}px;\n\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n\n  .anticon:first-of-type {\n    margin-right: ${4*t.gridUnit}px;\n  }\n\n  .anticon:nth-of-type(2) {\n    margin-left: ${4*t.gridUnit}px;\n  `}}
`,ze=v.iK.div`
  ${e=>{let{theme:t}=e;return`\n  margin-left: ${6*t.gridUnit}px;\n  margin-bottom: ${3*t.gridUnit}px;\n  font-weight: ${t.typography.weights.bold};\n  `}}
`,Oe=v.iK.div`
  ${e=>{let{theme:t}=e;return`\n  padding: ${8*t.gridUnit}px\n    ${6*t.gridUnit}px;\n  box-sizing: border-box;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 100%;\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  left: 0;\n  right: 0;\n  `}}
`,Ke=v.iK.div`
  ${e=>{let{theme:t}=e;return`\n  max-width: 50%;\n  width: 200px;\n\n  img {\n    width: 120px;\n    margin-left: 40px;\n  }\n\n  div {\n    width: 100%;\n    margin-top: ${3*t.gridUnit}px;\n    text-align: center;\n    font-weight: ${t.typography.weights.normal};\n    font-size: ${t.typography.sizes.l}px;\n    color: ${t.colors.grayscale.light1};\n  }\n  `}}
`,We=v.iK.div`
  ${e=>{let{theme:t}=e;return`\n  position: relative;\n  margin: ${3*t.gridUnit}px;\n  margin-left: ${6*t.gridUnit}px;\n  height: calc(100% - ${60*t.gridUnit}px);\n  overflow: auto;\n  `}}
`,De=v.iK.div`
  ${e=>{let{theme:t}=e;return`\n  position: relative;\n  margin: ${3*t.gridUnit}px;\n  margin-left: ${6*t.gridUnit}px;\n  height: calc(100% - ${30*t.gridUnit}px);\n  overflow: auto;\n  `}}
`,Ve=v.iK.div`
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
`,Fe=(0,v.iK)(Ze.Z)`
  ${e=>{let{theme:t}=e;return`\n  border: 1px solid ${t.colors.info.base};\n  padding: ${4*t.gridUnit}px;\n  margin: ${6*t.gridUnit}px ${6*t.gridUnit}px\n    ${8*t.gridUnit}px;\n  .view-dataset-button {\n    position: absolute;\n    top: ${4*t.gridUnit}px;\n    right: ${4*t.gridUnit}px;\n    font-weight: ${t.typography.weights.normal};\n\n    &:hover {\n      color: ${t.colors.secondary.dark3};\n      text-decoration: underline;\n    }\n  }\n  `}}
`,je=(0,r.t)("Refreshing columns"),Ae=(0,r.t)("Table columns"),He=(0,r.t)("Loading"),Be=["5","10","15","25"],qe=[{title:"Column Name",dataIndex:"name",key:"name",sorter:(e,t)=>we("name",e,t)},{title:"Datatype",dataIndex:"type",key:"type",width:"100px",sorter:(e,t)=>we("type",e,t)}],Xe=(0,r.t)("This table already has a dataset associated with it. You can only associate one dataset with a table.\n"),Ge=(0,r.t)("View Dataset"),Ye=e=>{var t;let{tableName:n,columnList:l,loading:i,hasError:o,datasets:s}=e;const d=(0,v.Fg)(),u=null!=(t=(null==l?void 0:l.length)>0)&&t,c=null==s?void 0:s.map((e=>e.table_name)),h=null==s?void 0:s.find((e=>e.table_name===n));let p,g;return i&&(g=(0,b.tZ)(Oe,null,(0,b.tZ)(Ke,null,(0,b.tZ)("img",{alt:He,src:$e}),(0,b.tZ)("div",null,je)))),i||(p=!i&&n&&u&&!o?(0,b.tZ)(a.Fragment,null,(0,b.tZ)(ze,null,Ae),h?(0,b.tZ)(We,null,(0,b.tZ)(Ve,null,(0,b.tZ)(H.ZP,{loading:i,size:H.ex.SMALL,columns:qe,data:l,pageSizeOptions:Be,defaultPageSize:25}))):(0,b.tZ)(De,null,(0,b.tZ)(Ve,null,(0,b.tZ)(H.ZP,{loading:i,size:H.ex.SMALL,columns:qe,data:l,pageSizeOptions:Be,defaultPageSize:25})))):(0,b.tZ)(Re,{hasColumns:u,hasError:o,tableName:n})),(0,b.tZ)(a.Fragment,null,n&&(0,b.tZ)(a.Fragment,null,(null==c?void 0:c.includes(n))&&(f=h,(0,b.tZ)(Fe,{closable:!1,type:"info",showIcon:!0,message:(0,r.t)("This table already has a dataset"),description:(0,b.tZ)(a.Fragment,null,Xe,(0,b.tZ)("span",{role:"button",onClick:()=>{window.open(null==f?void 0:f.explore_url,"_blank","noreferrer noopener popup=false")},tabIndex:0,className:"view-dataset-button"},Ge))})),(0,b.tZ)(Le,{position:!i&&u?Ne.RELATIVE:Ne.ABSOLUTE,title:n||""},n&&(0,b.tZ)(m.Z.Table,{iconColor:d.colors.grayscale.base}),n)),p,g);var f},Qe=e=>{let{tableName:t,dbId:n,schema:l,setHasColumns:s,datasets:d}=e;const[c,h]=(0,a.useState)([]),[p,g]=(0,a.useState)(!1),[m,f]=(0,a.useState)(!1),v=(0,a.useRef)(t);return(0,a.useEffect)((()=>{v.current=t,t&&l&&n&&(async e=>{const{dbId:t,tableName:n,schema:a}=e;g(!0),null==s||s(!1);const l=`/api/v1/database/${t}/table/${n}/${a}/`;try{const e=await i.Z.get({endpoint:l});if((e=>{let t=!0;if("string"!=typeof(null==e?void 0:e.name)&&(t=!1),t&&!Array.isArray(e.columns)&&(t=!1),t&&e.columns.length>0){const n=e.columns.some(((e,t)=>{const n=(e=>{let t=!0;const n="The object provided to isITableColumn does match the interface.";return"string"!=typeof(null==e?void 0:e.name)&&(t=!1,console.error(`${n} The property 'name' is required and must be a string`)),t&&"string"!=typeof(null==e?void 0:e.type)&&(t=!1,console.error(`${n} The property 'type' is required and must be a string`)),t})(e);return n||console.error(`The provided object does not match the IDatabaseTable interface. columns[${t}] is invalid and does not match the ITableColumn interface`),!n}));t=!n}return t})(null==e?void 0:e.json)){const t=e.json;t.name===v.current&&(h(t.columns),null==s||s(t.columns.length>0),f(!1))}else h([]),null==s||s(!1),f(!0),(0,u.Gb)((0,r.t)("The API response from %s does not match the IDatabaseTable interface.",l)),o.Z.error((0,r.t)("The API response from %s does not match the IDatabaseTable interface.",l))}catch(e){h([]),null==s||s(!1),f(!0)}finally{g(!1)}})({tableName:t,dbId:n,schema:l})}),[t,n,l]),(0,b.tZ)(Ye,{columnList:c,hasError:m,loading:p,tableName:t,datasets:d})};var Je=n(17982),et=n(61337);const tt=v.iK.div`
  ${e=>{let{theme:t}=e;return`\n    padding: ${4*t.gridUnit}px;\n    height: 100%;\n    background-color: ${t.colors.grayscale.light5};\n    position: relative;\n    .emptystate {\n      height: auto;\n      margin-top: ${17.5*t.gridUnit}px;\n    }\n    .section-title {\n      margin-top: ${5.5*t.gridUnit}px;\n      margin-bottom: ${11*t.gridUnit}px;\n      font-weight: ${t.typography.weights.bold};\n    }\n    .table-title {\n      margin-top: ${11*t.gridUnit}px;\n      margin-bottom: ${6*t.gridUnit}px;\n      font-weight: ${t.typography.weights.bold};\n    }\n    .options-list {\n      overflow: auto;\n      position: absolute;\n      bottom: 0;\n      top: ${92.25*t.gridUnit}px;\n      left: ${3.25*t.gridUnit}px;\n      right: 0;\n\n      .no-scrollbar {\n        margin-right: ${4*t.gridUnit}px;\n      }\n\n      .options {\n        cursor: pointer;\n        padding: ${1.75*t.gridUnit}px;\n        border-radius: ${t.borderRadius}px;\n        :hover {\n          background-color: ${t.colors.grayscale.light4}\n        }\n      }\n\n      .options-highlighted {\n        cursor: pointer;\n        padding: ${1.75*t.gridUnit}px;\n        border-radius: ${t.borderRadius}px;\n        background-color: ${t.colors.primary.dark1};\n        color: ${t.colors.grayscale.light5};\n      }\n\n      .options, .options-highlighted {\n        display: flex;\n        align-items: center;\n        justify-content: space-between;\n      }\n    }\n    form > span[aria-label="refresh"] {\n      position: absolute;\n      top: ${69*t.gridUnit}px;\n      left: ${42.75*t.gridUnit}px;\n      font-size: ${4.25*t.gridUnit}px;\n    }\n    .table-form {\n      margin-bottom: ${8*t.gridUnit}px;\n    }\n    .loading-container {\n      position: absolute;\n      top: ${89.75*t.gridUnit}px;\n      left: 0;\n      right: 0;\n      text-align: center;\n      img {\n        width: ${20*t.gridUnit}px;\n        margin-bottom: ${2.5*t.gridUnit}px;\n      }\n      p {\n        color: ${t.colors.grayscale.light1};\n      }\n    }\n`}}
`;function nt(e){let{setDataset:t,dataset:n,datasetNames:l}=e;const{addDangerToast:i}=(0,Y.e1)(),o=(0,a.useCallback)((e=>{t({type:h.selectDatabase,payload:{db:e}})}),[t]);(0,a.useEffect)((()=>{const e=(0,et.rV)(et.dR.db,null);e&&o(e)}),[o]);const s=(0,a.useCallback)((e=>(0,b.tZ)(Je.ez,{table:null!=l&&l.includes(e.value)?{...e,extra:{warning_markdown:(0,r.t)("This table already has a dataset")}}:e})),[l]);return(0,b.tZ)(tt,null,(0,b.tZ)(Je.ZP,(0,F.Z)({database:null==n?void 0:n.db,handleError:i,emptyState:(0,B.UX)(!1),onDbChange:o,onSchemaChange:e=>{e&&t({type:h.selectSchema,payload:{name:"schema",value:e}})},onTableSelectChange:e=>{t({type:h.selectTable,payload:{name:"table_name",value:e}})},sqlLabMode:!1,customTableOptionLabelRenderer:s},(null==n?void 0:n.schema)&&{schema:n.schema})))}var at=n(97381),lt=n(3741);const it=["db","schema","table_name"],rt=[lt.Ph,lt.FY,lt.Eh,lt.TA],ot=(0,Y.ZP)((function(e){let{datasetObject:t,addDangerToast:n,hasColumns:i=!1,datasets:o}=e;const s=(0,l.k6)(),{createResource:d}=(0,Q.LE)("dataset",(0,r.t)("dataset"),n),u=(0,r.t)("Select a database table."),c=(0,r.t)("Create dataset and create chart"),h=!(null!=t&&t.table_name)||!i||(null==o?void 0:o.includes(null==t?void 0:t.table_name));return(0,b.tZ)(a.Fragment,null,(0,b.tZ)(g.Z,{onClick:()=>{if(t){const e=(e=>{let t=0;const n=Object.keys(e).reduce(((n,a)=>(it.includes(a)&&e[a]&&(t+=1),t)),0);return rt[n]})(t);(0,at.logEvent)(e,t)}else(0,at.logEvent)(lt.Ph,{});s.goBack()}},(0,r.t)("Cancel")),(0,b.tZ)(g.Z,{buttonStyle:"primary",disabled:h,tooltip:null!=t&&t.table_name?void 0:u,onClick:()=>{if(t){var e;const n={database:null==(e=t.db)?void 0:e.id,schema:t.schema,table_name:t.table_name};d(n).then((e=>{e&&"number"==typeof e&&((0,at.logEvent)(lt.P$,t),s.push(`/chart/add/?dataset=${t.table_name}`))}))}}},c))}));var st=n(80663);function dt(e){let{header:t,leftPanel:n,datasetPanel:a,rightPanel:l,footer:i}=e;const r=(0,v.Fg)();return(0,b.tZ)(y,null,t&&(0,b.tZ)(E,null,t),(0,b.tZ)($,null,n&&(0,b.tZ)(st.Z,{id:"dataset",initialWidth:80*r.gridUnit,minWidth:80*r.gridUnit,enable:!0},(e=>(0,b.tZ)(x,{width:e},(0,b.tZ)(S,null,n)))),(0,b.tZ)(Z,null,(0,b.tZ)(U,null,a&&(0,b.tZ)(C,null,a),l&&(0,b.tZ)(P,null,l)),(0,b.tZ)(_,null,i&&(0,b.tZ)(k,null,i)))))}function ut(e,t){const n={...e||{}};switch(t.type){case h.selectDatabase:return{...n,...t.payload,schema:null,table_name:null};case h.selectSchema:return{...n,[t.payload.name]:t.payload.value,table_name:null};case h.selectTable:return{...n,[t.payload.name]:t.payload.value};case h.changeDataset:return{...n,[t.payload.name]:t.payload.value};default:return null}}const ct="/tablemodelview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc";function ht(){const[e,t]=(0,a.useReducer)(ut,null),[n,i]=(0,a.useState)(!1),[r,o]=(0,a.useState)(!1),{datasets:s,datasetNames:d}=c(null==e?void 0:e.db,null==e?void 0:e.schema),{datasetId:u}=(0,l.UO)();return(0,a.useEffect)((()=>{Number.isNaN(parseInt(u,10))||o(!0)}),[u]),(0,b.tZ)(dt,{header:(0,b.tZ)(O,{setDataset:t,title:null==e?void 0:e.table_name}),leftPanel:r?null:(0,b.tZ)(nt,{setDataset:t,dataset:e,datasetNames:d}),datasetPanel:r?(0,b.tZ)(xe,{id:u}):(0,b.tZ)(Qe,{tableName:null==e?void 0:e.table_name,dbId:null==e||null==(h=e.db)?void 0:h.id,schema:null==e?void 0:e.schema,setHasColumns:i,datasets:s}),footer:(0,b.tZ)(ot,{url:ct,datasetObject:e,hasColumns:n,datasets:d})});var h}}}]);
//# sourceMappingURL=07c1c231e16cb5fa43df.chunk.js.map