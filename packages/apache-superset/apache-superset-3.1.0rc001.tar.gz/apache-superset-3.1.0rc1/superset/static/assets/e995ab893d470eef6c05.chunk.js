"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[7001],{81788:(e,t,a)=>{a.d(t,{B8:()=>d,TZ:()=>o,mf:()=>l,u7:()=>r});var s=a(31069),n=a(68492);const i=(e,t,a)=>{let s=`api/v1/dashboard/${e}/filter_state`;return t&&(s=s.concat(`/${t}`)),a&&(s=s.concat(`?tab_id=${a}`)),s},o=(e,t,a,o)=>s.Z.put({endpoint:i(e,a,o),jsonPayload:{value:t}}).then((e=>e.json.message)).catch((e=>(n.Z.error(e),null))),r=(e,t,a)=>s.Z.post({endpoint:i(e,void 0,a),jsonPayload:{value:t}}).then((e=>e.json.key)).catch((e=>(n.Z.error(e),null))),d=(e,t)=>s.Z.get({endpoint:i(e,t)}).then((e=>{let{json:t}=e;return JSON.parse(t.value)})).catch((e=>(n.Z.error(e),null))),l=e=>s.Z.get({endpoint:`/api/v1/dashboard/permalink/${e}`}).then((e=>{let{json:t}=e;return t})).catch((e=>(n.Z.error(e),null)))},57001:(e,t,a)=>{a.r(t),a.d(t,{DashboardPage:()=>re,DashboardPageIdContext:()=>ne,default:()=>de});var s=a(67294),n=a(11965),i=a(16550),o=a(51995),r=a(93185),d=a(78161),l=a(28062),c=a(61988),u=a(28216),p=a(14114),h=a(38703),g=a(67417),m=a(4305),f=a(50810),v=a(14505),b=a(7241),y=a(61337),_=a(27600),w=a(23525),S=a(52794),E=a(9467),x=a(81788),D=a(14890),C=a(45697),T=a.n(C),I=a(14278),R=a(20292),j=a(81255);function F(e){return Object.values(e).reduce(((e,t)=>(t&&t.type===j.dW&&t.meta&&t.meta.chartId&&e.push(t.meta.chartId),e)),[])}var O=a(2275),$=a(3741),U=a(99543),Z=a(56967);const k=[j.dW,j.xh,j.t];function q(e){return!Object.values(e).some((e=>{let{type:t}=e;return t&&k.includes(t)}))}const L={actions:T().shape({addSliceToDashboard:T().func.isRequired,removeSliceFromDashboard:T().func.isRequired,triggerQuery:T().func.isRequired,logEvent:T().func.isRequired,clearDataMaskState:T().func.isRequired}).isRequired,dashboardInfo:O.$X.isRequired,dashboardState:O.DZ.isRequired,slices:T().objectOf(O.Rw).isRequired,activeFilters:T().object.isRequired,chartConfiguration:T().object,datasources:T().object.isRequired,ownDataCharts:T().object.isRequired,layout:T().object.isRequired,impressionId:T().string.isRequired,initMessages:T().array,timeout:T().number,userId:T().string};class M extends s.PureComponent{static onBeforeUnload(e){e?window.addEventListener("beforeunload",M.unload):window.removeEventListener("beforeunload",M.unload)}static unload(){const e=(0,c.t)("You have unsaved changes.");return window.event.returnValue=e,e}constructor(e){var t,a;super(e),this.appliedFilters=null!=(t=e.activeFilters)?t:{},this.appliedOwnDataCharts=null!=(a=e.ownDataCharts)?a:{},this.onVisibilityChange=this.onVisibilityChange.bind(this)}componentDidMount(){const e=(0,R.Z)(),{dashboardState:t,layout:a}=this.props,s={is_soft_navigation:$.Yd.timeOriginOffset>0,is_edit_mode:t.editMode,mount_duration:$.Yd.getTimestamp(),is_empty:q(a),is_published:t.isPublished,bootstrap_data_length:e.length},n=(0,Z.Z)();n&&(s.target_id=n),this.props.actions.logEvent($.Wl,s),"hidden"===document.visibilityState&&(this.visibilityEventData={start_offset:$.Yd.getTimestamp(),ts:(new Date).getTime()}),window.addEventListener("visibilitychange",this.onVisibilityChange),this.applyCharts()}componentDidUpdate(){this.applyCharts()}UNSAFE_componentWillReceiveProps(e){const t=F(this.props.layout),a=F(e.layout);this.props.dashboardInfo.id===e.dashboardInfo.id&&(t.length<a.length?a.filter((e=>-1===t.indexOf(e))).forEach((t=>{return this.props.actions.addSliceToDashboard(t,(a=e.layout,s=t,Object.values(a).find((e=>e&&e.type===j.dW&&e.meta&&e.meta.chartId===s))));var a,s})):t.length>a.length&&t.filter((e=>-1===a.indexOf(e))).forEach((e=>this.props.actions.removeSliceFromDashboard(e))))}applyCharts(){const{hasUnsavedChanges:e,editMode:t}=this.props.dashboardState,{appliedFilters:a,appliedOwnDataCharts:s}=this,{activeFilters:n,ownDataCharts:i,chartConfiguration:o}=this.props;(0,r.cr)(r.TT.DASHBOARD_CROSS_FILTERS)&&!o||(t||(0,U.JB)(s,i,{ignoreUndefined:!0})&&(0,U.JB)(a,n,{ignoreUndefined:!0})||this.applyFilters(),e?M.onBeforeUnload(!0):M.onBeforeUnload(!1))}componentWillUnmount(){window.removeEventListener("visibilitychange",this.onVisibilityChange),this.props.actions.clearDataMaskState()}onVisibilityChange(){if("hidden"===document.visibilityState)this.visibilityEventData={start_offset:$.Yd.getTimestamp(),ts:(new Date).getTime()};else if("visible"===document.visibilityState){const e=this.visibilityEventData.start_offset;this.props.actions.logEvent($.Ev,{...this.visibilityEventData,duration:$.Yd.getTimestamp()-e})}}applyFilters(){const{appliedFilters:e}=this,{activeFilters:t,ownDataCharts:a}=this.props,s=Object.keys(t),n=Object.keys(e),i=new Set(s.concat(n)),o=((e,t)=>{const a=Object.keys(e),s=Object.keys(t),n=(i=a,o=s,[...i.filter((e=>!o.includes(e))),...o.filter((e=>!i.includes(e)))]).filter((a=>e[a]||t[a]));var i,o;return new Set([...a,...s]).forEach((a=>{(0,U.JB)(e[a],t[a])||n.push(a)})),[...new Set(n)]})(a,this.appliedOwnDataCharts);[...i].forEach((a=>{if(!s.includes(a)&&n.includes(a))o.push(...e[a].scope);else if(n.includes(a)){if((0,U.JB)(e[a].values,t[a].values,{ignoreUndefined:!0})||o.push(...t[a].scope),!(0,U.JB)(e[a].scope,t[a].scope)){const s=(t[a].scope||[]).concat(e[a].scope||[]);o.push(...s)}}else o.push(...t[a].scope)})),this.refreshCharts([...new Set(o)]),this.appliedFilters=t,this.appliedOwnDataCharts=a}refreshCharts(e){e.forEach((e=>{this.props.actions.triggerQuery(!0,e)}))}render(){return this.context.loading?(0,n.tZ)(h.Z,null):this.props.children}}M.contextType=I.Zn,M.propTypes=L,M.defaultProps={initMessages:[],timeout:60,userId:""};const B=M;var P=a(52256),J=a(97381),N=a(43399),V=a(87915),A=a(74599);const Y=(0,u.$j)((function(e){var t,a,s,n,i;const{datasources:o,sliceEntities:r,dataMask:d,dashboardInfo:l,dashboardState:c,dashboardLayout:u,impressionId:p,nativeFilters:h}=e;return{initMessages:null==(t=l.common)?void 0:t.flash_messages,timeout:null==(a=l.common)||null==(s=a.conf)?void 0:s.SUPERSET_WEBSERVER_TIMEOUT,userId:l.userId,dashboardInfo:l,dashboardState:c,datasources:o,activeFilters:{...(0,N.De)(),...(0,V.g)({chartConfiguration:null==(n=l.metadata)?void 0:n.chart_configuration,nativeFilters:h.filters,dataMask:d,allSliceIds:c.sliceIds})},chartConfiguration:null==(i=l.metadata)?void 0:i.chart_configuration,ownDataCharts:(0,V.U)(d,"ownState"),slices:r.slices,layout:u.present,impressionId:p}}),(function(e){return{actions:(0,D.DE)({setDatasources:f.Fy,clearDataMaskState:A.sh,addSliceToDashboard:E.Pi,removeSliceFromDashboard:E.rL,triggerQuery:P.triggerQuery,logEvent:J.logEvent},e)}}))(B);var Q=a(14670),z=a.n(Q);const W=e=>n.iv`
  body {
    h1 {
      font-weight: ${e.typography.weights.bold};
      line-height: 1.4;
      font-size: ${e.typography.sizes.xxl}px;
      letter-spacing: -0.2px;
      margin-top: ${3*e.gridUnit}px;
      margin-bottom: ${3*e.gridUnit}px;
    }

    h2 {
      font-weight: ${e.typography.weights.bold};
      line-height: 1.4;
      font-size: ${e.typography.sizes.xl}px;
      margin-top: ${3*e.gridUnit}px;
      margin-bottom: ${2*e.gridUnit}px;
    }

    h3,
    h4,
    h5,
    h6 {
      font-weight: ${e.typography.weights.bold};
      line-height: 1.4;
      font-size: ${e.typography.sizes.l}px;
      letter-spacing: 0.2px;
      margin-top: ${2*e.gridUnit}px;
      margin-bottom: ${e.gridUnit}px;
    }
  }
`,K=e=>n.iv`
  .filter-card-popover {
    width: 240px;
    padding: 0;
    border-radius: 4px;

    &.ant-popover-placement-bottom {
      padding-top: ${e.gridUnit}px;
    }

    &.ant-popover-placement-left {
      padding-right: ${3*e.gridUnit}px;
    }

    .ant-popover-inner {
      box-shadow: 0 0 8px rgb(0 0 0 / 10%);
    }

    .ant-popover-inner-content {
      padding: ${4*e.gridUnit}px;
    }

    .ant-popover-arrow {
      display: none;
    }
  }

  .filter-card-tooltip {
    &.ant-tooltip-placement-bottom {
      padding-top: 0;
      & .ant-tooltip-arrow {
        top: -13px;
      }
    }
  }
`,H=e=>n.iv`
  .ant-dropdown-menu.chart-context-menu {
    min-width: ${43*e.gridUnit}px;
  }
  .ant-dropdown-menu-submenu.chart-context-submenu {
    max-width: ${60*e.gridUnit}px;
    min-width: ${40*e.gridUnit}px;
  }
`;var X=a(78718),G=a.n(X);const ee={},te=()=>{const e=(0,y.rV)(y.dR.dashboard__explore_context,{});return Object.fromEntries(Object.entries(e).filter((e=>{let[,t]=e;return!t.isRedundant})))},ae=(e,t)=>{const a=te();(0,y.LS)(y.dR.dashboard__explore_context,{...a,[e]:t})},se=e=>{let{dashboardPageId:t}=e;const a=(0,u.v9)((e=>{var a,s,n;let{dashboardInfo:i,dashboardState:o,nativeFilters:r,dataMask:d}=e;return{labelColors:(null==(a=i.metadata)?void 0:a.label_colors)||ee,sharedLabelColors:(null==(s=i.metadata)?void 0:s.shared_label_colors)||ee,colorScheme:null==o?void 0:o.colorScheme,chartConfiguration:(null==(n=i.metadata)?void 0:n.chart_configuration)||ee,nativeFilters:Object.entries(r.filters).reduce(((e,t)=>{let[a,s]=t;return{...e,[a]:G()(s,["chartsInScope"])}}),{}),dataMask:d,dashboardId:i.id,filterBoxFilters:(0,N.De)(),dashboardPageId:t}}),u.wU);return(0,s.useEffect)((()=>(ae(t,a),()=>{ae(t,{...a,isRedundant:!0})})),[a,t]),null},ne=s.createContext("");(0,b.Z)();const ie=s.lazy((()=>Promise.all([a.e(1216),a.e(9612),a.e(1247),a.e(8),a.e(981),a.e(9258),a.e(5640),a.e(3197),a.e(95),a.e(868),a.e(1880),a.e(8149),a.e(4717),a.e(452)]).then(a.bind(a,24406)))),oe=document.title,re=e=>{let{idOrSlug:t}=e;const a=(0,o.Fg)(),b=(0,u.I0)(),D=(0,i.k6)(),C=(0,s.useMemo)((()=>z().generate()),[]),T=(0,u.v9)((e=>{let{dashboardInfo:t}=e;return t&&Object.keys(t).length>0})),{addDangerToast:I}=(0,p.e1)(),{result:R,error:j}=(0,g.QU)(t),{result:F,error:O}=(0,g.Es)(t),{result:$,error:U,status:Z}=(0,g.JL)(t),k=(0,s.useRef)(!1),q=j||O,L=Boolean(R&&F),{dashboard_title:M,css:B,metadata:P,id:J=0}=R||{},N=(0,r.cr)(r.TT.DASHBOARD_NATIVE_FILTERS_SET)&&(0,r.cr)(r.TT.DASHBOARD_NATIVE_FILTERS);if((0,s.useEffect)((()=>{const e=()=>{const e=te();(0,y.LS)(y.dR.dashboard__explore_context,{...e,[C]:{...e[C],isRedundant:!0}})};return window.addEventListener("beforeunload",e),()=>{window.removeEventListener("beforeunload",e)}}),[C]),(0,s.useEffect)((()=>{b((0,E.sL)(Z))}),[b,Z]),(0,s.useEffect)((()=>{J&&async function(){const e=(0,w.eY)(_.KD.permalinkKey),t=(0,w.eY)(_.KD.nativeFiltersKey),a=(0,w.eY)(_.KD.nativeFilters);let s,n=t||{};if(e){const t=await(0,x.mf)(e);t&&({dataMask:n,activeTabs:s}=t.state)}else t&&(n=await(0,x.B8)(J,t));a&&(n=a),L&&(k.current||(k.current=!0,N&&b((0,S.pi)(J))),b((0,m.Y)({history:D,dashboard:R,charts:F,activeTabs:s,dataMask:n})))}()}),[L]),(0,s.useEffect)((()=>(M&&(document.title=M),()=>{document.title=oe})),[M]),(0,s.useEffect)((()=>"string"==typeof B?(0,v.Z)(B):()=>{}),[B]),(0,s.useEffect)((()=>{const e=(0,d.ZP)();return e.source=d.Ag.dashboard,()=>{l.getNamespace(null==P?void 0:P.color_namespace).resetColors(),e.clear()}}),[null==P?void 0:P.color_namespace]),(0,s.useEffect)((()=>{U?I((0,c.t)("Error loading chart datasources. Filters may not work correctly.")):b((0,f.Fy)($))}),[I,$,U,b]),q)throw q;return L&&T?(0,n.tZ)(s.Fragment,null,(0,n.tZ)(n.xB,{styles:[K(a),W(a),H(a),"",""]}),(0,n.tZ)(se,{dashboardPageId:C}),(0,n.tZ)(ne.Provider,{value:C},(0,n.tZ)(Y,null,(0,n.tZ)(ie,null)))):(0,n.tZ)(h.Z,null)},de=re},87915:(e,t,a)=>{a.d(t,{U:()=>s,g:()=>n});const s=(e,t)=>Object.values(e).filter((e=>e[t])).reduce(((e,a)=>({...e,[a.id]:t?a[t]:a})),{}),n=e=>{let{chartConfiguration:t,nativeFilters:a,dataMask:s,allSliceIds:n}=e;const i={};return Object.values(s).forEach((e=>{var s,o,r,d,l,c;let{id:u,extraFormData:p}=e;const h=null!=(s=null!=(o=null!=(r=null==a||null==(d=a[u])?void 0:d.chartsInScope)?r:null==t||null==(l=t[u])||null==(c=l.crossFilters)?void 0:c.chartsInScope)?o:n)?s:[];i[u]={scope:h,values:p}})),i}},14505:(e,t,a)=>{function s(e){const t="CssEditor-css",a=document.head||document.getElementsByTagName("head")[0],s=document.querySelector(`.${t}`)||function(e){const t=document.createElement("style");return t.className=e,t.type="text/css",t}(t);return"styleSheet"in s?s.styleSheet.cssText=e:s.innerHTML=e,a.appendChild(s),function(){s.remove()}}a.d(t,{Z:()=>s})},67417:(e,t,a)=>{a.d(t,{schemaEndpoints:()=>h.Kt,CN:()=>s.CN,tableEndpoints:()=>p.QD,hb:()=>d,QU:()=>l,Es:()=>c,JL:()=>u,L8:()=>m,Xx:()=>h.Xx,SJ:()=>p.SJ,uY:()=>p.uY,zA:()=>p.zA});var s=a(45673),n=a(42190),i=a(15926);function o(e){let{owners:t}=e;return t?t.map((e=>`${e.first_name} ${e.last_name}`)):null}const r=a.n(i)().encode({columns:["owners.first_name","owners.last_name"],keys:["none"]});function d(e){return(0,n.l6)((0,n.s_)(`/api/v1/chart/${e}?q=${r}`),o)}const l=e=>(0,n.l6)((0,n.s_)(`/api/v1/dashboard/${e}`),(e=>({...e,metadata:e.json_metadata&&JSON.parse(e.json_metadata)||{},position_data:e.position_json&&JSON.parse(e.position_json)}))),c=e=>(0,n.s_)(`/api/v1/dashboard/${e}/charts`),u=e=>(0,n.s_)(`/api/v1/dashboard/${e}/datasets`);var p=a(23936),h=a(69279);const g=a(10362).h.injectEndpoints({endpoints:e=>({queryValidations:e.query({providesTags:["QueryValidations"],query:e=>{let{dbId:t,schema:a,sql:s,templateParams:n}=e,i=n;try{i=JSON.parse(n||"")}catch(e){i=void 0}const o={schema:a,sql:s,...i&&{template_params:i}};return{method:"post",endpoint:`/api/v1/database/${t}/validate_sql/`,headers:{"Content-Type":"application/json"},body:JSON.stringify(o),transformResponse:e=>{let{json:t}=e;return t.result}}}})})}),{useQueryValidationsQuery:m}=g}}]);
//# sourceMappingURL=e995ab893d470eef6c05.chunk.js.map