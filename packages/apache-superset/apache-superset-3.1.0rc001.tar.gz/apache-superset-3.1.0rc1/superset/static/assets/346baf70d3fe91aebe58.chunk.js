"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9173],{27989:(e,t,a)=>{a.d(t,{Z:()=>m});var r=a(67294),n=a(51995),l=a(61988),s=a(35932),o=a(74069),i=a(4715),d=a(34858),u=a(60972),c=a(11965);const p=n.iK.div`
  display: block;
  color: ${e=>{let{theme:t}=e;return t.colors.grayscale.base}};
  font-size: ${e=>{let{theme:t}=e;return t.typography.sizes.s}}px;
`,h=n.iK.div`
  padding-bottom: ${e=>{let{theme:t}=e;return 2*t.gridUnit}}px;
  padding-top: ${e=>{let{theme:t}=e;return 2*t.gridUnit}}px;

  & > div {
    margin: ${e=>{let{theme:t}=e;return t.gridUnit}}px 0;
  }

  &.extra-container {
    padding-top: 8px;
  }

  .confirm-overwrite {
    margin-bottom: ${e=>{let{theme:t}=e;return 2*t.gridUnit}}px;
  }

  .input-container {
    display: flex;
    align-items: center;

    label {
      display: flex;
      margin-right: ${e=>{let{theme:t}=e;return 2*t.gridUnit}}px;
    }

    i {
      margin: 0 ${e=>{let{theme:t}=e;return t.gridUnit}}px;
    }
  }

  input,
  textarea {
    flex: 1 1 auto;
  }

  textarea {
    height: 160px;
    resize: none;
  }

  input::placeholder,
  textarea::placeholder {
    color: ${e=>{let{theme:t}=e;return t.colors.grayscale.light1}};
  }

  textarea,
  input[type='text'],
  input[type='number'] {
    padding: ${e=>{let{theme:t}=e;return 1.5*t.gridUnit}}px
      ${e=>{let{theme:t}=e;return 2*t.gridUnit}}px;
    border-style: none;
    border: 1px solid ${e=>{let{theme:t}=e;return t.colors.grayscale.light2}};
    border-radius: ${e=>{let{theme:t}=e;return t.gridUnit}}px;

    &[name='name'] {
      flex: 0 1 auto;
      width: 40%;
    }

    &[name='sqlalchemy_uri'] {
      margin-right: ${e=>{let{theme:t}=e;return 3*t.gridUnit}}px;
    }
  }
`,m=e=>{let{resourceName:t,resourceLabel:a,passwordsNeededMessage:n,confirmOverwriteMessage:m,onModelImport:g,show:y,onHide:v,passwordFields:b=[],setPasswordFields:Z=(()=>{}),sshTunnelPasswordFields:w=[],setSSHTunnelPasswordFields:f=(()=>{}),sshTunnelPrivateKeyFields:S=[],setSSHTunnelPrivateKeyFields:x=(()=>{}),sshTunnelPrivateKeyPasswordFields:k=[],setSSHTunnelPrivateKeyPasswordFields:T=(()=>{})}=e;const[_,$]=(0,r.useState)(!0),[q,C]=(0,r.useState)({}),[P,N]=(0,r.useState)(!1),[D,E]=(0,r.useState)(!1),[F,H]=(0,r.useState)([]),[K,I]=(0,r.useState)(!1),[R,z]=(0,r.useState)(),[L,O]=(0,r.useState)({}),[U,A]=(0,r.useState)({}),[M,Q]=(0,r.useState)({}),B=()=>{H([]),Z([]),C({}),N(!1),E(!1),I(!1),z(""),f([]),x([]),T([]),O({}),A({}),Q({})},{state:{alreadyExists:Y,passwordsNeeded:j,sshPasswordNeeded:G,sshPrivateKeyNeeded:V,sshPrivateKeyPasswordNeeded:W},importResource:X}=(0,d.PW)(t,a,(e=>{z(e)}));(0,r.useEffect)((()=>{Z(j),j.length>0&&I(!1)}),[j,Z]),(0,r.useEffect)((()=>{N(Y.length>0),Y.length>0&&I(!1)}),[Y,N]),(0,r.useEffect)((()=>{f(G),G.length>0&&I(!1)}),[G,f]),(0,r.useEffect)((()=>{x(V),V.length>0&&I(!1)}),[V,x]),(0,r.useEffect)((()=>{T(W),W.length>0&&I(!1)}),[W,T]);return _&&y&&$(!1),(0,c.tZ)(o.default,{name:"model",className:"import-model-modal",disablePrimaryButton:0===F.length||P&&!D||K,onHandledPrimaryAction:()=>{var e;(null==(e=F[0])?void 0:e.originFileObj)instanceof File&&(I(!0),X(F[0].originFileObj,q,L,U,M,D).then((e=>{e&&(B(),g())})))},onHide:()=>{$(!0),v(),B()},primaryButtonName:P?(0,l.t)("Overwrite"):(0,l.t)("Import"),primaryButtonType:P?"danger":"primary",width:"750px",show:y,title:(0,c.tZ)("h4",null,(0,l.t)("Import %s",a))},(0,c.tZ)(h,null,(0,c.tZ)(i.gq,{name:"modelFile",id:"modelFile",accept:".yaml,.json,.yml,.zip",fileList:F,onChange:e=>{H([{...e.file,status:"done"}])},onRemove:e=>(H(F.filter((t=>t.uid!==e.uid))),!1),customRequest:()=>{},disabled:K},(0,c.tZ)(s.Z,{loading:K},(0,l.t)("Select file")))),R&&(0,c.tZ)(u.Z,{errorMessage:R,showDbInstallInstructions:b.length>0||w.length>0||S.length>0||k.length>0}),(()=>{if(0===b.length&&0===w.length&&0===S.length&&0===k.length)return null;const e=[...new Set([...b,...w,...S,...k])];return(0,c.tZ)(r.Fragment,null,(0,c.tZ)("h5",null,(0,l.t)("Database passwords")),(0,c.tZ)(p,null,n),e.map((e=>(0,c.tZ)(r.Fragment,null,(null==b?void 0:b.indexOf(e))>=0&&(0,c.tZ)(h,{key:`password-for-${e}`},(0,c.tZ)("div",{className:"control-label"},(0,l.t)("%s PASSWORD",e.slice(10)),(0,c.tZ)("span",{className:"required"},"*")),(0,c.tZ)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:q[e],onChange:t=>C({...q,[e]:t.target.value})})),(null==w?void 0:w.indexOf(e))>=0&&(0,c.tZ)(h,{key:`ssh_tunnel_password-for-${e}`},(0,c.tZ)("div",{className:"control-label"},(0,l.t)("%s SSH TUNNEL PASSWORD",e.slice(10)),(0,c.tZ)("span",{className:"required"},"*")),(0,c.tZ)("input",{name:`ssh_tunnel_password-${e}`,autoComplete:`ssh_tunnel_password-${e}`,type:"password",value:L[e],onChange:t=>O({...L,[e]:t.target.value})})),(null==S?void 0:S.indexOf(e))>=0&&(0,c.tZ)(h,{key:`ssh_tunnel_private_key-for-${e}`},(0,c.tZ)("div",{className:"control-label"},(0,l.t)("%s SSH TUNNEL PRIVATE KEY",e.slice(10)),(0,c.tZ)("span",{className:"required"},"*")),(0,c.tZ)("textarea",{name:`ssh_tunnel_private_key-${e}`,autoComplete:`ssh_tunnel_private_key-${e}`,value:U[e],onChange:t=>A({...U,[e]:t.target.value})})),(null==k?void 0:k.indexOf(e))>=0&&(0,c.tZ)(h,{key:`ssh_tunnel_private_key_password-for-${e}`},(0,c.tZ)("div",{className:"control-label"},(0,l.t)("%s SSH TUNNEL PRIVATE KEY PASSWORD",e.slice(10)),(0,c.tZ)("span",{className:"required"},"*")),(0,c.tZ)("input",{name:`ssh_tunnel_private_key_password-${e}`,autoComplete:`ssh_tunnel_private_key_password-${e}`,type:"password",value:M[e],onChange:t=>Q({...M,[e]:t.target.value})}))))))})(),P?(0,c.tZ)(r.Fragment,null,(0,c.tZ)(h,null,(0,c.tZ)("div",{className:"confirm-overwrite"},m),(0,c.tZ)("div",{className:"control-label"},(0,l.t)('Type "%s" to confirm',(0,l.t)("OVERWRITE"))),(0,c.tZ)("input",{id:"overwrite",type:"text",onChange:e=>{var t,a;const r=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";E(r.toUpperCase()===(0,l.t)("OVERWRITE"))}}))):null)}},29848:(e,t,a)=>{a.d(t,{Z:()=>d}),a(67294);var r=a(51995),n=a(58593),l=a(70707),s=a(11965);const o=r.iK.span`
  white-space: nowrap;
  min-width: 100px;
  svg,
  i {
    margin-right: 8px;

    &:hover {
      path {
        fill: ${e=>{let{theme:t}=e;return t.colors.primary.base}};
      }
    }
  }
`,i=r.iK.span`
  color: ${e=>{let{theme:t}=e;return t.colors.grayscale.base}};
`;function d(e){let{actions:t}=e;return(0,s.tZ)(o,{className:"actions"},t.map(((e,t)=>{const a=l.Z[e.icon];return e.tooltip?(0,s.tZ)(n.u,{id:`${e.label}-tooltip`,title:e.tooltip,placement:e.placement,key:t},(0,s.tZ)(i,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick},(0,s.tZ)(a,null))):(0,s.tZ)(i,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick,key:t},(0,s.tZ)(a,null))})))}},83556:(e,t,a)=>{a.d(t,{P:()=>c});var r=a(67294),n=a(51995),l=a(59361),s=a(58593),o=a(11965);const i=(0,n.iK)(l.Z)`
  ${e=>{let{theme:t}=e;return`\n  margin-top: ${t.gridUnit}px;\n  margin-bottom: ${t.gridUnit}px;\n  font-size: ${t.typography.sizes.s}px;\n  `}};
`,d=e=>{let{name:t,id:a,index:n,onDelete:l,editable:d=!1,onClick:u,toolTipTitle:c=t}=e;const p=(0,r.useMemo)((()=>t.length>20),[t])?`${t.slice(0,20)}...`:t;return(0,o.tZ)(r.Fragment,null,d?(0,o.tZ)(s.u,{title:c,key:c},(0,o.tZ)(i,{key:a,closable:d,onClose:()=>n?null==l?void 0:l(n):null,color:"blue"},p)):(0,o.tZ)(s.u,{title:c,key:c},(0,o.tZ)(i,{role:"link",key:a,onClick:u},a?(0,o.tZ)("a",{href:`/superset/all_entities/?id=${a}`,target:"_blank",rel:"noreferrer"},p):p)))},u=n.iK.div`
  max-width: 100%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
`,c=e=>{let{tags:t,editable:a=!1,onDelete:n,maxTags:l}=e;const[s,i]=(0,r.useState)(l),c=e=>{null==n||n(e)},p=(0,r.useMemo)((()=>s?t.length>s:null),[t.length,s]),h=(0,r.useMemo)((()=>"number"==typeof s?t.length-s+1:null),[p,t.length,s]);return(0,o.tZ)(u,{className:"tag-list"},p&&"number"==typeof s?(0,o.tZ)(r.Fragment,null,t.slice(0,s-1).map(((e,t)=>(0,o.tZ)(d,{id:e.id,key:e.id,name:e.name,index:t,onDelete:c,editable:a}))),t.length>s?(0,o.tZ)(d,{name:`+${h}...`,onClick:()=>i(void 0),toolTipTitle:t.map((e=>e.name)).join(", ")}):null):(0,o.tZ)(r.Fragment,null,t.map(((e,t)=>(0,o.tZ)(d,{id:e.id,key:e.id,name:e.name,index:t,onDelete:c,editable:a}))),l&&t.length>l?(0,o.tZ)(d,{name:"...",onClick:()=>i(l)}):null))}},33726:(e,t,a)=>{a.d(t,{Y:()=>n});var r=a(61988);const n={name:(0,r.t)("SQL"),tabs:[{name:"Saved queries",label:(0,r.t)("Saved queries"),url:"/savedqueryview/list/",usesRouter:!0},{name:"Query history",label:(0,r.t)("Query history"),url:"/sqllab/history/",usesRouter:!0}]}},6189:(e,t,a)=>{a.d(t,{Z:()=>y});var r=a(73126),n=(a(67294),a(51995)),l=a(61988),s=a(33743),o=a(49889),i=a(53459),d=a(22489),u=a(120),c=a(42110),p=a(70707),h=a(10222),m=a(11965);c.Z.registerLanguage("sql",s.Z),c.Z.registerLanguage("markdown",i.Z),c.Z.registerLanguage("html",o.Z),c.Z.registerLanguage("json",d.Z);const g=n.iK.div`
  margin-top: -24px;

  &:hover {
    svg {
      visibility: visible;
    }
  }

  svg {
    position: relative;
    top: 40px;
    left: 512px;
    visibility: hidden;
    margin: -4px;
    color: ${e=>{let{theme:t}=e;return t.colors.grayscale.base}};
  }
`;function y(e){let{addDangerToast:t,addSuccessToast:a,children:n,...s}=e;return(0,m.tZ)(g,null,(0,m.tZ)(p.Z.Copy,{tabIndex:0,role:"button",onClick:e=>{var r;e.preventDefault(),e.currentTarget.blur(),r=n,(0,h.Z)((()=>Promise.resolve(r))).then((()=>{a&&a((0,l.t)("SQL Copied!"))})).catch((()=>{t&&t((0,l.t)("Sorry, your browser does not support copying."))}))}}),(0,m.tZ)(c.Z,(0,r.Z)({style:u.Z},s),n))}},86185:(e,t,a)=>{a.d(t,{Z:()=>n});var r=a(67294);function n(e){let{queries:t,fetchData:a,currentQueryId:n}=e;const l=t.findIndex((e=>e.id===n)),[s,o]=(0,r.useState)(l),[i,d]=(0,r.useState)(!1),[u,c]=(0,r.useState)(!1);function p(){d(0===s),c(s===t.length-1)}function h(e){const r=s+(e?-1:1);r>=0&&r<t.length&&(a(t[r].id),o(r),p())}return(0,r.useEffect)((()=>{p()})),{handleKeyPress:function(e){s>=0&&s<t.length&&("ArrowDown"===e.key||"k"===e.key?(e.preventDefault(),h(!1)):"ArrowUp"!==e.key&&"j"!==e.key||(e.preventDefault(),h(!0)))},handleDataChange:h,disablePrevious:i,disableNext:u}}},7742:(e,t,a)=>{a.r(t),a.d(t,{default:()=>B});var r=a(61988),n=a(51995),l=a(93185),s=a(31069),o=a(67294),i=a(16550),d=a(73727),u=a(15926),c=a.n(u),p=a(30381),h=a.n(p),m=a(40768),g=a(28216),y=a(99299),v=a(14114),b=a(34858),Z=a(19259),w=a(32228),f=a(86074),S=a(93139),x=a(38703),k=a(17198),T=a(29848),_=a(83556),$=a(58593),q=a(33726),C=a(10222),P=a(27989),N=a(70707),D=a(74069),E=a(35932),F=a(6189),H=a(86185),K=a(11965);const I=n.iK.div`
  color: ${e=>{let{theme:t}=e;return t.colors.secondary.light2}};
  font-size: ${e=>{let{theme:t}=e;return t.typography.sizes.s}}px;
  margin-bottom: 0;
  text-transform: uppercase;
`,R=n.iK.div`
  color: ${e=>{let{theme:t}=e;return t.colors.grayscale.dark2}};
  font-size: ${e=>{let{theme:t}=e;return t.typography.sizes.m}}px;
  padding: 4px 0 16px 0;
`,z=(0,n.iK)(D.default)`
  .ant-modal-content {
  }

  .ant-modal-body {
    padding: 24px;
  }

  pre {
    font-size: ${e=>{let{theme:t}=e;return t.typography.sizes.xs}}px;
    font-weight: ${e=>{let{theme:t}=e;return t.typography.weights.normal}};
    line-height: ${e=>{let{theme:t}=e;return t.typography.sizes.l}}px;
    height: 375px;
    border: none;
  }
`,L=(0,v.ZP)((e=>{let{fetchData:t,onHide:a,openInSqlLab:n,queries:l,savedQuery:s,show:i,addDangerToast:d,addSuccessToast:u}=e;const{handleKeyPress:c,handleDataChange:p,disablePrevious:h,disableNext:m}=(0,H.Z)({queries:l,currentQueryId:s.id,fetchData:t});return(0,K.tZ)("div",{role:"none",onKeyUp:c},(0,K.tZ)(z,{onHide:a,show:i,title:(0,r.t)("Query preview"),footer:(0,K.tZ)(o.Fragment,null,(0,K.tZ)(E.Z,{key:"previous-saved-query",disabled:h,onClick:()=>p(!0)},(0,r.t)("Previous")),(0,K.tZ)(E.Z,{key:"next-saved-query",disabled:m,onClick:()=>p(!1)},(0,r.t)("Next")),(0,K.tZ)(E.Z,{key:"open-in-sql-lab",buttonStyle:"primary",onClick:e=>{let{metaKey:t}=e;return n(s.id,Boolean(t))}},(0,r.t)("Open in SQL Lab")))},(0,K.tZ)(I,null,(0,r.t)("Query name")),(0,K.tZ)(R,null,s.label),(0,K.tZ)(F.Z,{language:"sql",addDangerToast:d,addSuccessToast:u},s.sql||"")))}));var O=a(12617);const U=(0,r.t)('The passwords for the databases below are needed in order to import them together with the saved queries. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in export files, and should be added manually after the import if they are needed.'),A=(0,r.t)("You are importing one or more saved queries that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?"),M=n.iK.div`
  .count {
    margin-left: 5px;
    color: ${e=>{let{theme:t}=e;return t.colors.primary.base}};
    text-decoration: underline;
    cursor: pointer;
  }
`,Q=n.iK.div`
  color: ${e=>{let{theme:t}=e;return t.colors.grayscale.dark2}};
`,B=(0,v.ZP)((function(e){let{addDangerToast:t,addSuccessToast:a}=e;const{state:{loading:n,resourceCount:u,resourceCollection:p,bulkSelectEnabled:v},hasPerm:D,fetchData:E,toggleBulkSelect:F,refreshData:H}=(0,b.Yi)("saved_query",(0,r.t)("Saved queries"),t),{roles:I}=(0,g.v9)((e=>e.user)),R=(0,O.R)("can_read","Tag",I),[z,B]=(0,o.useState)(null),[Y,j]=(0,o.useState)(null),[G,V]=(0,o.useState)(!1),[W,X]=(0,o.useState)([]),[J,ee]=(0,o.useState)(!1),[te,ae]=(0,o.useState)([]),[re,ne]=(0,o.useState)([]),[le,se]=(0,o.useState)([]),oe=(0,i.k6)(),ie=D("can_write"),de=D("can_write"),ue=D("can_write"),ce=D("can_export")&&(0,l.cr)(l.TT.VERSIONED_EXPORT),pe=(0,o.useCallback)((e=>{s.Z.get({endpoint:`/api/v1/saved_query/${e}`}).then((e=>{let{json:t={}}=e;j({...t.result})}),(0,m.v$)((e=>t((0,r.t)("There was an issue previewing the selected query %s",e)))))}),[t]),he={activeChild:"Saved queries",...q.Y},me=[];ue&&me.push({name:(0,r.t)("Bulk select"),onClick:F,buttonStyle:"secondary"}),me.push({name:(0,K.tZ)(d.rU,{to:"/sqllab?new=true"},(0,K.tZ)("i",{className:"fa fa-plus"})," ",(0,r.t)("Query")),buttonStyle:"primary"}),ie&&(0,l.cr)(l.TT.VERSIONED_EXPORT)&&me.push({name:(0,K.tZ)($.u,{id:"import-tooltip",title:(0,r.t)("Import queries"),placement:"bottomRight"},(0,K.tZ)(N.Z.Import,null)),buttonStyle:"link",onClick:()=>{V(!0)},"data-test":"import-button"}),he.buttons=me;const ge=(e,t)=>{t?window.open(`/sqllab?savedQueryId=${e}`):oe.push(`/sqllab?savedQueryId=${e}`)},ye=(0,o.useCallback)((e=>{(0,C.Z)((()=>Promise.resolve(`${window.location.origin}/sqllab?savedQueryId=${e}`))).then((()=>{a((0,r.t)("Link Copied!"))})).catch((()=>{t((0,r.t)("Sorry, your browser does not support copying."))}))}),[t,a]),ve=e=>{const t=e.map((e=>{let{id:t}=e;return t}));(0,w.Z)("saved_query",t,(()=>{ee(!1)})),ee(!0)},be=[{id:"changed_on_delta_humanized",desc:!0}],Ze=(0,o.useMemo)((()=>[{accessor:"label",Header:(0,r.t)("Name")},{accessor:"database.database_name",Header:(0,r.t)("Database"),size:"xl"},{accessor:"database",hidden:!0,disableSortBy:!0},{accessor:"schema",Header:(0,r.t)("Schema"),size:"xl"},{Cell:e=>{let{row:{original:{sql_tables:t=[]}}}=e;const a=t.map((e=>e.table)),n=(null==a?void 0:a.shift())||"";return a.length?(0,K.tZ)(M,null,(0,K.tZ)("span",null,n),(0,K.tZ)(y.Z,{placement:"right",title:(0,r.t)("TABLES"),trigger:"click",content:(0,K.tZ)(o.Fragment,null,a.map((e=>(0,K.tZ)(Q,{key:e},e))))},(0,K.tZ)("span",{className:"count"},"(+",a.length,")"))):n},accessor:"sql_tables",Header:(0,r.t)("Tables"),size:"xl",disableSortBy:!0},{Cell:e=>{let{row:{original:{created_on:t}}}=e;const a=new Date(t),r=new Date(Date.UTC(a.getFullYear(),a.getMonth(),a.getDate(),a.getHours(),a.getMinutes(),a.getSeconds(),a.getMilliseconds()));return h()(r).fromNow()},Header:(0,r.t)("Created on"),accessor:"created_on",size:"xl"},{Cell:e=>{let{row:{original:{changed_on_delta_humanized:t}}}=e;return t},Header:(0,r.t)("Modified"),accessor:"changed_on_delta_humanized",size:"xl"},{Cell:e=>{let{row:{original:{tags:t=[]}}}=e;return(0,K.tZ)(_.P,{tags:t.filter((e=>1===e.type))})},Header:(0,r.t)("Tags"),accessor:"tags",disableSortBy:!0,hidden:!(0,l.cr)(l.TT.TAGGING_SYSTEM)},{Cell:e=>{let{row:{original:t}}=e;const a=[{label:"preview-action",tooltip:(0,r.t)("Query preview"),placement:"bottom",icon:"Binoculars",onClick:()=>{pe(t.id)}},de&&{label:"edit-action",tooltip:(0,r.t)("Edit query"),placement:"bottom",icon:"Edit",onClick:e=>{let{metaKey:a}=e;return ge(t.id,Boolean(a))}},{label:"copy-action",tooltip:(0,r.t)("Copy query URL"),placement:"bottom",icon:"Copy",onClick:()=>ye(t.id)},ce&&{label:"export-action",tooltip:(0,r.t)("Export query"),placement:"bottom",icon:"Share",onClick:()=>ve([t])},ue&&{label:"delete-action",tooltip:(0,r.t)("Delete query"),placement:"bottom",icon:"Trash",onClick:()=>B(t)}].filter((e=>!!e));return(0,K.tZ)(T.Z,{actions:a})},Header:(0,r.t)("Actions"),id:"actions",disableSortBy:!0}]),[ue,de,ce,ye,pe]),we=(0,o.useMemo)((()=>[{Header:(0,r.t)("Database"),key:"database",id:"database",input:"select",operator:S.p.relationOneMany,unfilteredLabel:(0,r.t)("All"),fetchSelects:(0,m.tm)("saved_query","database",(0,m.v$)((e=>t((0,r.t)("An error occurred while fetching dataset datasource values: %s",e))))),paginate:!0},{Header:(0,r.t)("Schema"),id:"schema",key:"schema",input:"select",operator:S.p.equals,unfilteredLabel:"All",fetchSelects:(0,m.wk)("saved_query","schema",(0,m.v$)((e=>t((0,r.t)("An error occurred while fetching schema values: %s",e))))),paginate:!0},{Header:(0,r.t)("Search"),id:"label",key:"search",input:"search",operator:S.p.allText}]),[t]);return(0,l.cr)(l.TT.TAGGING_SYSTEM)&&R&&we.push({Header:(0,r.t)("Tags"),id:"tags",key:"tags",input:"search",operator:S.p.savedQueryTags}),(0,K.tZ)(o.Fragment,null,(0,K.tZ)(f.Z,he),z&&(0,K.tZ)(k.Z,{description:(0,r.t)("This action will permanently delete the saved query."),onConfirm:()=>{z&&(e=>{let{id:n,label:l}=e;s.Z.delete({endpoint:`/api/v1/saved_query/${n}`}).then((()=>{H(),B(null),a((0,r.t)("Deleted: %s",l))}),(0,m.v$)((e=>t((0,r.t)("There was an issue deleting %s: %s",l,e)))))})(z)},onHide:()=>B(null),open:!0,title:(0,r.t)("Delete Query?")}),Y&&(0,K.tZ)(L,{fetchData:pe,onHide:()=>j(null),savedQuery:Y,queries:p,openInSqlLab:ge,show:!0}),(0,K.tZ)(Z.Z,{title:(0,r.t)("Please confirm"),description:(0,r.t)("Are you sure you want to delete the selected queries?"),onConfirm:e=>{s.Z.delete({endpoint:`/api/v1/saved_query/?q=${c().encode(e.map((e=>{let{id:t}=e;return t})))}`}).then((e=>{let{json:t={}}=e;H(),a(t.message)}),(0,m.v$)((e=>t((0,r.t)("There was an issue deleting the selected queries: %s",e)))))}},(e=>{const l=[];return ue&&l.push({key:"delete",name:(0,r.t)("Delete"),onSelect:e,type:"danger"}),ce&&l.push({key:"export",name:(0,r.t)("Export"),type:"primary",onSelect:ve}),(0,K.tZ)(S.Z,{className:"saved_query-list-view",columns:Ze,count:u,data:p,fetchData:E,filters:we,initialSort:be,loading:n,pageSize:25,bulkActions:l,addSuccessToast:a,addDangerToast:t,bulkSelectEnabled:v,disableBulkSelect:F,highlightRowId:null==Y?void 0:Y.id,enableBulkTag:!0,bulkTagResourceName:"query",refreshData:H})})),(0,K.tZ)(P.Z,{resourceName:"saved_query",resourceLabel:(0,r.t)("queries"),passwordsNeededMessage:U,confirmOverwriteMessage:A,addDangerToast:t,addSuccessToast:a,onModelImport:()=>{V(!1),H(),a((0,r.t)("Query imported"))},show:G,onHide:()=>{V(!1)},passwordFields:W,setPasswordFields:X,sshTunnelPasswordFields:te,setSSHTunnelPasswordFields:ae,sshTunnelPrivateKeyFields:re,setSSHTunnelPrivateKeyFields:ne,sshTunnelPrivateKeyPasswordFields:le,setSSHTunnelPrivateKeyPasswordFields:se}),J&&(0,K.tZ)(x.Z,null))}))}}]);
//# sourceMappingURL=346baf70d3fe91aebe58.chunk.js.map