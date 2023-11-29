"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[1880],{32871:(t,e,i)=>{var n;i.d(e,{p:()=>n}),function(t){t.DASHBOARDS="dashboards",t.DESCRIPTION="description",t.LAST_MODIFIED="lastModified",t.OWNER="owner",t.ROWS="rows",t.SQL="sql",t.TABLE="table",t.TAGS="tags"}(n||(n={}))},67697:(t,e,i)=>{i.d(e,{pG:()=>x.p,ZP:()=>Z});var n=i(87185),l=i.n(n),r=i(67294),a=i(99612),o=i(51995),s=i(58593),d=i(55786),c=i(61988),p=i(70707),u=i(11965);const h=o.iK.div`
  font-weight: ${t=>{let{theme:e}=t;return e.typography.weights.bold}};
`,f=t=>{let{text:e,header:i}=t;const n=(0,d.Z)(e);return(0,u.tZ)(r.Fragment,null,i&&(0,u.tZ)(h,null,i),n.map((t=>(0,u.tZ)("div",{key:t},t))))},g=16,m={dashboards:0,table:1,sql:2,rows:3,tags:4,description:5,owner:6,lastModified:7},v=o.iK.div`
  ${t=>{let{theme:e,count:i}=t;return`\n    display: flex;\n    align-items: center;\n    padding: 8px 12px;\n    background-color: ${e.colors.grayscale.light4};\n    color: ${e.colors.grayscale.base};\n    font-size: ${e.typography.sizes.s}px;\n    min-width: ${24+32*i-g}px;\n    border-radius: ${e.borderRadius}px;\n    line-height: 1;\n  `}}
`,w=o.iK.div`
  ${t=>{let{theme:e,collapsed:i,last:n,onClick:l}=t;return`\n    display: flex;\n    align-items: center;\n    max-width: ${174+(n?0:g)}px;\n    min-width: ${i?16+(n?0:g):94+(n?0:g)}px;\n    padding-right: ${n?0:g}px;\n    cursor: ${l?"pointer":"default"};\n    & .metadata-icon {\n      color: ${l&&i?e.colors.primary.base:e.colors.grayscale.base};\n      padding-right: ${i?0:8}px;\n      & .anticon {\n        line-height: 0;\n      }\n    }\n    & .metadata-text {\n      min-width: 70px;\n      overflow: hidden;\n      text-overflow: ${i?"unset":"ellipsis"};\n      white-space: nowrap;\n      text-decoration: ${l?"underline":"none"};\n      line-height: 1.4;\n    }\n  `}}
`,y=o.iK.div`
  display: -webkit-box;
  -webkit-line-clamp: 20;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
`,b=t=>{let{barWidth:e,contentType:i,collapsed:n,last:l=!1,tooltipPlacement:a}=t;const{icon:o,title:d,tooltip:h=d}=(t=>{const{type:e}=t;switch(e){case x.p.DASHBOARDS:return{icon:p.Z.FundProjectionScreenOutlined,title:t.title,tooltip:t.description?(0,u.tZ)("div",null,(0,u.tZ)(f,{header:t.title,text:t.description})):void 0};case x.p.DESCRIPTION:return{icon:p.Z.BookOutlined,title:t.value};case x.p.LAST_MODIFIED:return{icon:p.Z.EditOutlined,title:t.value,tooltip:(0,u.tZ)("div",null,(0,u.tZ)(f,{header:(0,c.t)("Last modified"),text:t.value}),(0,u.tZ)(f,{header:(0,c.t)("Modified by"),text:t.modifiedBy}))};case x.p.OWNER:return{icon:p.Z.UserOutlined,title:t.createdBy,tooltip:(0,u.tZ)("div",null,(0,u.tZ)(f,{header:(0,c.t)("Created by"),text:t.createdBy}),!!t.owners&&(0,u.tZ)(f,{header:(0,c.t)("Owners"),text:t.owners}),(0,u.tZ)(f,{header:(0,c.t)("Created on"),text:t.createdOn}))};case x.p.ROWS:return{icon:p.Z.InsertRowBelowOutlined,title:t.title,tooltip:t.title};case x.p.SQL:return{icon:p.Z.ConsoleSqlOutlined,title:t.title,tooltip:t.title};case x.p.TABLE:return{icon:p.Z.Table,title:t.title,tooltip:t.title};case x.p.TAGS:return{icon:p.Z.TagsOutlined,title:t.values.join(", "),tooltip:(0,u.tZ)("div",null,(0,u.tZ)(f,{header:(0,c.t)("Tags"),text:t.values}))};default:throw Error(`Invalid type provided: ${e}`)}})(i),[g,m]=(0,r.useState)(!1),v=(0,r.useRef)(null),b=o,{type:Z,onClick:$}=i;(0,r.useEffect)((()=>{m(!!v.current&&v.current.scrollWidth>v.current.clientWidth)}),[e,m,i]);const S=(0,u.tZ)(w,{collapsed:n,last:l,onClick:$?()=>$(Z):void 0},(0,u.tZ)(b,{iconSize:"l",className:"metadata-icon"}),!n&&(0,u.tZ)("span",{ref:v,className:"metadata-text"},d));return g||n||h&&h!==d?(0,u.tZ)(s.u,{placement:a,title:(0,u.tZ)(y,null,h)},S):S};var x=i(32871);const Z=t=>{let{items:e,tooltipPlacement:i="top"}=t;const[n,o]=(0,r.useState)(),[s,d]=(0,r.useState)(!1),c=l()(e,((t,e)=>t.type===e.type)).sort(((t,e)=>m[t.type]-m[e.type])),p=c.length;if(p<2)throw Error("The minimum number of items for the metadata bar is 2.");if(p>6)throw Error("The maximum number of items for the metadata bar is 6.");const h=(0,r.useCallback)((t=>{const e=110*p-g;o(t),d(Boolean(t&&t<e))}),[p]),{ref:f}=(0,a.NB)({onResize:h});return(0,u.tZ)(v,{ref:f,count:p},c.map(((t,e)=>(0,u.tZ)(b,{barWidth:n,key:e,contentType:t,collapsed:s,last:e===p-1,tooltipPlacement:i}))))}},52564:(t,e,i)=>{i.d(e,{u:()=>x});var n=i(73126),l=i(67294),r=i(11965),a=i(51995),o=i(61988),s=i(4715),d=i(58593),c=i(99612);const p=t=>r.iv`
  display: flex;
  font-size: ${t.typography.sizes.xl}px;
  font-weight: ${t.typography.weights.bold};
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
      color: ${t.colors.grayscale.light1};
    }
  }

  & .input-sizer {
    position: absolute;
    left: -9999px;
    display: inline-block;
  }
`,u=t=>{let{title:e,placeholder:i,onSave:n,canEdit:a,label:s}=t;const[u,h]=(0,l.useState)(!1),[f,g]=(0,l.useState)(e||""),m=(0,l.useRef)(null),[v,w]=(0,l.useState)(!1),{width:y,ref:b}=(0,c.NB)(),{width:x,ref:Z}=(0,c.NB)({refreshMode:"debounce"});(0,l.useEffect)((()=>{g(e)}),[e]),(0,l.useEffect)((()=>{if(u&&null!=m&&m.current&&(m.current.focus(),m.current.setSelectionRange)){const{length:t}=m.current.value;m.current.setSelectionRange(t,t),m.current.scrollLeft=m.current.scrollWidth}}),[u]),(0,l.useLayoutEffect)((()=>{null!=b&&b.current&&(b.current.innerHTML=(f||i).replace(/\s/g,"&nbsp;"))}),[f,i,b]),(0,l.useEffect)((()=>{m.current&&m.current.scrollWidth>m.current.clientWidth?w(!0):w(!1)}),[y,x]);const $=(0,l.useCallback)((()=>{a&&!u&&h(!0)}),[a,u]),S=(0,l.useCallback)((()=>{if(!a)return;const t=f.trim();g(t),e!==t&&n(t),h(!1)}),[a,f,n,e]),k=(0,l.useCallback)((t=>{a&&u&&g(t.target.value)}),[a,u]),T=(0,l.useCallback)((t=>{var e;a&&"Enter"===t.key&&(t.preventDefault(),null==(e=m.current)||e.blur())}),[a]);return(0,r.tZ)("div",{css:p,ref:Z},(0,r.tZ)(d.u,{id:"title-tooltip",title:v&&f&&!u?f:null},a?(0,r.tZ)("input",{className:"dynamic-title-input","aria-label":null!=s?s:(0,o.t)("Title"),ref:m,onChange:k,onBlur:S,onClick:$,onKeyPress:T,placeholder:i,value:f,css:r.iv`
              cursor: ${u?"text":"pointer"};

              ${y&&y>0&&r.iv`
                width: ${y+1}px;
              `}
            `}):(0,r.tZ)("span",{className:"dynamic-title","aria-label":null!=s?s:(0,o.t)("Title"),ref:m},f)),(0,r.tZ)("span",{ref:b,className:"input-sizer","aria-hidden":!0,tabIndex:-1}))};var h=i(79789),f=i(36674),g=i(70707),m=i(35932);const v=t=>r.iv`
  width: ${8*t.gridUnit}px;
  height: ${8*t.gridUnit}px;
  padding: 0;
  border: 1px solid ${t.colors.primary.dark2};

  &.ant-btn > span.anticon {
    line-height: 0;
    transition: inherit;
  }

  &:hover:not(:focus) > span.anticon {
    color: ${t.colors.primary.light1};
  }
`,w=t=>r.iv`
  display: flex;
  flex-direction: row;
  align-items: center;
  flex-wrap: nowrap;
  justify-content: space-between;
  background-color: ${t.colors.grayscale.light5};
  height: ${16*t.gridUnit}px;
  padding: 0 ${4*t.gridUnit}px;

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
    margin-right: ${12*t.gridUnit}px;
  }

  .right-button-panel {
    display: flex;
    align-items: center;
  }
`,y=t=>r.iv`
  display: flex;
  align-items: center;
  padding-left: ${2*t.gridUnit}px;

  & .fave-unfave-icon {
    padding: 0 ${t.gridUnit}px;

    &:first-of-type {
      padding-left: 0;
    }
  }
`,b=t=>r.iv`
  margin-left: ${2*t.gridUnit}px;
`,x=t=>{let{editableTitleProps:e,showTitlePanelItems:i,certificatiedBadgeProps:l,showFaveStar:d,faveStarProps:c,titlePanelAdditionalItems:p,rightPanelAdditionalItems:x,additionalActionsMenu:Z,menuDropdownProps:$,showMenuDropdown:S=!0,tooltipProps:k}=t;const T=(0,a.Fg)();return(0,r.tZ)("div",{css:w,className:"header-with-actions"},(0,r.tZ)("div",{className:"title-panel"},(0,r.tZ)(u,e),i&&(0,r.tZ)("div",{css:y},(null==l?void 0:l.certifiedBy)&&(0,r.tZ)(h.Z,l),d&&(0,r.tZ)(f.Z,c),p)),(0,r.tZ)("div",{className:"right-button-panel"},x,(0,r.tZ)("div",{css:b},S&&(0,r.tZ)(s.Gj,(0,n.Z)({trigger:["click"],overlay:Z},$),(0,r.tZ)(m.Z,{css:v,buttonStyle:"tertiary","aria-label":(0,o.t)("Menu actions trigger"),tooltip:null==k?void 0:k.text,placement:null==k?void 0:k.placement},(0,r.tZ)(g.Z.MoreHoriz,{iconColor:T.colors.primary.dark2,iconSize:"l"}))))))}}}]);
//# sourceMappingURL=6c725272457abdfac880.chunk.js.map