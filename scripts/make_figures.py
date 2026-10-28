from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ["MPLCONFIGDIR"]=str(ROOT/"_work/cache/matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager
import numpy as np
import json, shutil, sys

C={"ink":"#192634","blue":"#2c5282","rust":"#a24a2c","green":"#2f6f4e",
   "gray":"#64748b","pale":"#edf2f7","light":"#dce4ed"}
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,
 "axes.edgecolor":C["gray"],"axes.labelcolor":C["ink"],"text.color":C["ink"],
 "xtick.color":C["gray"],"ytick.color":C["gray"],"axes.titleweight":"bold",
 "savefig.facecolor":"white","svg.fonttype":"path","pdf.fonttype":42})
manifest=[]
def tr(lang,en,zh):return zh if lang=="zh" else en
def setup(lang):
    plt.rcParams["font.family"]="SimSun" if lang=="zh" else "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"]=False
def save(fig,name,lang):
    if len(sys.argv)>1 and name not in sys.argv[1:]:
        plt.close(fig)
        return
    out=ROOT/"shared/figures"/lang;out.mkdir(parents=True,exist_ok=True)
    for ext in ["pdf","svg","png"]:
        target=out/(name+"."+ext)
        fig.savefig(target,dpi=190,bbox_inches="tight",pad_inches=0.12)
        dest=ROOT/("en/assets" if lang=="en" else "zh/figures")/target.name
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,dest)
    plt.close(fig)
    manifest.append({"name":name,"language":lang,"source":"analytical model / schematic",
                     "path":f"shared/figures/{lang}/{name}.pdf"})
def box(ax,xy,w,h,label,color="blue",size=10):
    x,y=xy
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.025,rounding_size=0.07",
      facecolor="white",edgecolor=C[color],linewidth=1.4))
    ax.text(x+w/2,y+h/2,label,ha="center",va="center",fontsize=size,color=C[color])
def arrow(ax,a,b,color="gray",rad=0,lw=1.3):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=12,
      linewidth=lw,color=C[color],connectionstyle=f"arc3,rad={rad}",
      shrinkA=2,shrinkB=2))

for lang in ["en","zh"]:
    setup(lang)
    # Same endpoints, different kinetic barriers.
    fig,ax=plt.subplots(figsize=(7,3.7))
    x=np.linspace(0,1,700)
    base=-2*(3*x*x-2*x**3)
    h=np.sin(np.pi*x)**2
    for amp,col,lab in [(6,"rust",tr(lang,"Higher-barrier path","高势垒路径")),
                        (3.0,"blue",tr(lang,"Catalyzed path","催化路径"))]:
        ax.plot(x,base+amp*h,lw=2.4,color=C[col],label=lab)
    ax.scatter([0,1],[0,-2],color=C["ink"],s=30,zorder=5)
    ax.hlines([0,-2],0,1,colors=C["light"],linestyles="--")
    ax.annotate("",xy=(1.04,0),xytext=(1.04,-2),
      arrowprops=dict(arrowstyle="<->",color=C["green"],lw=1.4))
    ax.text(1.065,-1,r"$\Delta G$",va="center",color=C["green"])
    ax.set(xlim=(-.05,1.2),ylim=(-2.5,5.6),
      xlabel=tr(lang,"Reaction coordinate","反应坐标"),
      ylabel=tr(lang,"Free energy (schematic units)","自由能（示意单位）"))
    ax.set_xticks([0,1],labels=[tr(lang,"Reactants","反应物"),tr(lang,"Products","产物")])
    ax.legend(frameon=False,loc="upper right",fontsize=9)
    ax.set_title(tr(lang,"A better route lowers the barrier, not the endpoint difference",
                            "更好的路径降低势垒，起终态自由能差保持相同"),fontsize=11,pad=12)
    fig.tight_layout();save(fig,"activation-barrier",lang)

    # Three response forms: deliberately no empirical sector assignment.
    fig,ax=plt.subplots(figsize=(7,3.7))
    x=np.linspace(0,6,400)
    for y,col,lab in [(x,"blue",tr(lang,"Proportional","近似比例")),
       (2.5*(1-np.exp(-x/1.2)),"green",tr(lang,"Saturation","饱和")),
       (2.6*x*np.exp(-x/1.3),"rust",tr(lang,"Overload","过载后回落"))]:
        ax.plot(x,y,lw=2.3,color=C[col],label=lab)
    ax.set(xlabel=tr(lang,"Attempted input rate","尝试投入速率"),
           ylabel=tr(lang,"Useful output rate","有效产出速率"),xlim=(0,6),ylim=(0,6.2))
    ax.legend(frameon=False,loc="upper left")
    ax.set_title(tr(lang,"Measure the response before extrapolating the input",
       "外推投入之前，先辨认响应曲线"),fontsize=11,pad=12)
    ax.grid(alpha=.15);fig.tight_layout();save(fig,"response-regimes",lang)

    # Model changes action, and thereby its own evidence.
    fig,ax=plt.subplots(figsize=(8.2,3.6));ax.set(xlim=(0,12),ylim=(0,5));ax.axis("off")
    box(ax,(.35,2.8),2.1,1.0,tr(lang,"Model  m","模型  m"))
    box(ax,(3.25,2.8),2.15,1.0,tr(lang,"Action  a = π(m)","动作  a = π(m)"))
    box(ax,(6.25,2.8),2.15,1.0,tr(lang,"Receiving world","接收行动的世界"))
    box(ax,(9.2,2.8),2.3,1.0,tr(lang,"Evidence","响应证据"))
    for a,b in [((2.45,3.3),(3.25,3.3)),((5.4,3.3),(6.25,3.3)),
                 ((8.4,3.3),(9.2,3.3))]:arrow(ax,a,b)
    ax.plot([10.35,10.35,1.4],[2.8,1.8,1.8],color=C["blue"],lw=1.4)
    arrow(ax,(1.4,1.8),(1.4,2.8),"blue")
    ax.text(6.0,1.45,tr(lang,"Update U combines retained state, action, and observed response",
                             "更新 U 综合原有状态、动作及观测到的响应"),ha="center",fontsize=10)
    ax.text(6,.55,r"$DF=U_m+U_a\,D\pi$",ha="center",fontsize=19,color=C["rust"])
    ax.text(6,4.5,tr(lang,"The policy is inside the feedback derivative",
                         "策略本身也在反馈导数之内"),ha="center",fontsize=12,weight="bold")
    fig.tight_layout();save(fig,"model-action-loop",lang)

    # Fixed area ideal hover: energy added by battery, mass penalty nonlinear.
    fig,axs=plt.subplots(1,2,figsize=(8.1,3.8))
    x=np.linspace(0,7,500);p=(1+x)**1.5;t=x/p
    axs[0].plot(x,p,lw=2.5,color=C["rust"])
    axs[0].set(ylabel=r"$P/P_0=(1+x)^{3/2}$",ylim=(0,24))
    axs[1].plot(x,t,lw=2.5,color=C["blue"])
    axs[1].axvline(2,color=C["gray"],lw=1,ls="--")
    axs[1].scatter([2],[2/3**1.5],color=C["rust"],zorder=4,s=35)
    axs[1].annotate(tr(lang,"Model maximum: x = 2","模型极值：x = 2"),
      xy=(2,2/3**1.5),xytext=(3.0,.30),fontsize=9,
      arrowprops=dict(arrowstyle="-",color=C["gray"]))
    axs[1].set(ylabel=r"$t/t_0=x/(1+x)^{3/2}$",ylim=(0,.44))
    for ax in axs:
        ax.set(xlim=(0,7),xlabel=tr(lang,"Battery / non-battery mass  x","电池质量 / 非电池质量  x"))
        ax.grid(alpha=.15)
    axs[0].set_title(tr(lang,"Power grows with total mass","功率随总质量上升"),fontsize=11)
    axs[1].set_title(tr(lang,"Added energy meets its own weight","新增能量也要搬运自己"),fontsize=11)
    fig.tight_layout(w_pad=2.0);save(fig,"hover-tradeoff",lang)

    # Negative diagonal is insufficient for a multidimensional maximum.
    fig,axs=plt.subplots(1,2,figsize=(8,3.8))
    z=np.linspace(-1,1,240);X,Y=np.meshgrid(z,z)
    Z1=-X*X-Y*Y;Z2=-X*X-Y*Y+4*X*Y
    for ax,Z,title in zip(axs,[Z1,Z2],[
       tr(lang,"Strict local maximum","严格局部极大"),
       tr(lang,"Saddle despite negative diagonal","对角项均负，仍可为鞍点")]):
        ax.contour(X,Y,Z,levels=9,colors=C["blue"],linewidths=.9)
        ax.scatter([0],[0],c=C["rust"],s=25,zorder=4)
        ax.set(xlabel="x",ylabel="y",xlim=(-1,1),ylim=(-1,1),aspect="equal")
        ax.set_title(title,fontsize=10)
    arrow(axs[1],(.04,.04),(.8,.8),"rust",lw=1.8)
    axs[0].text(.5,-.27,r"$V=-x^2-y^2$",transform=axs[0].transAxes,ha="center",fontsize=12)
    axs[1].text(.5,-.27,r"$V=-x^2-y^2+4xy$",transform=axs[1].transAxes,ha="center",fontsize=12)
    fig.subplots_adjust(bottom=.26,wspace=.5);save(fig,"hessian-directions",lang)

    # Escape loss is a path-specific score dip, not a universal barrier.
    fig,ax=plt.subplots(figsize=(7,3.7))
    x=np.linspace(0,1,500);y=1-1.8*np.sin(np.pi*x)**2+.6*x**3
    ix=np.argmin(y);ax.plot(x,y,color=C["blue"],lw=2.5)
    ax.axhline(1,color=C["light"],ls="--")
    ax.hlines(y[ix],x[ix],.68,color=C["light"],ls="--")
    ax.annotate("",xy=(.68,1),xytext=(.68,y[ix]),
      arrowprops=dict(arrowstyle="<->",color=C["rust"],lw=1.5))
    ax.text(.71,.1,r"$\Delta V_{\rm loss}$",color=C["rust"],fontsize=12)
    ax.scatter([0,x[ix],1],[1,y[ix],1.6],color=C["ink"],s=28,zorder=4)
    ax.set(xlim=(-.04,1.07),ylim=(-1,1.9),xlabel=tr(lang,"Progress along a chosen path","沿选定路径的进度"),
      ylabel=tr(lang,"Value of the current score V","当前指标 V"))
    ax.set_title(tr(lang,"A better destination can require a worse interim score",
                       "更好的终点，也可能经过指标下降的过渡"),fontsize=11,pad=12)
    ax.set_xticks([0,1],labels=[tr(lang,"Start","起点"),tr(lang,"Destination","终点")])
    fig.tight_layout();save(fig,"escape-valley",lang)

    # Four functions share an event and can proceed in parallel.
    fig,ax=plt.subplots(figsize=(8.0,4.7));ax.set(xlim=(0,12),ylim=(0,7));ax.axis("off")
    box(ax,(.4,4.9),2.65,1.1,tr(lang,"Action → consequence","行动 → 后果"),"ink",10)
    box(ax,(4.2,4.9),3.1,1.1,tr(lang,"Discovery\nmonitor + report","发现\n监测 + 报告"),"blue",11)
    box(ax,(8.5,4.9),3.1,1.1,tr(lang,"Containment\ninterrupt + isolate","止损\n暂停 + 隔离"),"rust",11)
    box(ax,(4.2,2.75),3.1,1.1,tr(lang,"Traceability\nversions + decisions","追溯\n版本 + 决定"),"blue",11)
    box(ax,(8.5,2.75),3.1,1.1,tr(lang,"Remedy\ncorrect + compensate","救济\n纠错 + 补偿"),"green",11)
    arrow(ax,(3.05,5.45),(4.2,5.45))
    arrow(ax,(7.3,5.45),(8.5,5.45),"rust")
    arrow(ax,(5.75,4.9),(5.75,3.85),"blue")
    arrow(ax,(7.3,3.3),(8.5,3.3),"green")
    arrow(ax,(10.05,4.9),(10.05,3.85),"gray")
    ax.plot([10.05,10.05,1.72,1.72],[2.75,1.6,1.6,4.7],color=C["gray"],lw=1.2)
    arrow(ax,(1.72,4.65),(1.72,4.9))
    ax.text(6.0,.95,tr(lang,"Named actors + usable authority + records + resources",
       "明确主体 + 实际权限 + 可用记录 + 承担资源"),ha="center",fontsize=11)
    ax.text(6.0,6.65,tr(lang,"Consequences need a route into response",
       "让后果进入回应"),ha="center",fontsize=12,weight="bold")
    fig.tight_layout();save(fig,"accountability",lang)

    # A nondominated but unsupported point.
    fig,ax=plt.subplots(figsize=(6.7,4))
    ax.plot([0,3],[3,0],color=C["gray"],lw=1.3,ls="--",
      label=tr(lang,"Convex-hull boundary","凸包边界"))
    for name,(xx,yy),col in [("A",(0,3),"blue"),("B",(1,1),"rust"),("C",(3,0),"blue")]:
        ax.scatter([xx],[yy],s=65,color=C[col],zorder=5)
        ax.text(xx+.10,yy+.10,f"{name} ({xx}, {yy})",fontsize=10,color=C[col])
    ax.text(1.18,2.65,tr(lang,"Maximize both dimensions","两个维度均取大为优"),fontsize=10)
    ax.text(1.55,1.85,tr(lang,"B is Pareto-efficient\nbut no positive linear weight selects it",
       "B 是帕累托有效点\n正线性权重却不会选中它"),fontsize=9,color=C["rust"])
    ax.set(xlim=(-.3,3.85),ylim=(-.3,3.55),
      xlabel=tr(lang,"Value 1","价值 1"),ylabel=tr(lang,"Value 2","价值 2"))
    ax.set_xticks(range(4));ax.set_yticks(range(4));ax.grid(alpha=.15)
    ax.legend(frameon=False,loc="lower left",fontsize=9)
    fig.tight_layout();save(fig,"unsupported-pareto",lang)

    # Linearized delayed logistic, r=1. Numerical method of steps.
    fig,axs=plt.subplots(1,2,figsize=(8.2,3.5))
    dt=.002;t=np.arange(0,32+dt,dt)
    for ax,delay in zip(axs,[.8,1.8]):
        u=np.zeros_like(t);u[0]=.05
        for i in range(1,len(t)):
            q=t[i-1]-delay
            past=.05 if q<=0 else np.interp(q,t[:i],u[:i])
            u[i]=u[i-1]-dt*past
        ax.plot(t,u,color=C["blue"] if delay<1 else C["rust"],lw=1.7)
        ax.axhline(0,color=C["gray"],lw=.7)
        ax.set(xlabel=tr(lang,"Scaled time  rt","无量纲时间  rt"),
          ylabel=tr(lang,"Small perturbation  u","小扰动  u"),xlim=(0,32),ylim=(-.32,.32))
        ax.set_title(f"rθ = {delay}  "+tr(lang,"(decay)" if delay<1 else "(growth)",
          "（衰减）" if delay<1 else "（放大）"),fontsize=11)
        ax.grid(alpha=.15)
    fig.tight_layout(w_pad=2);save(fig,"delay-stability",lang)

    # Dependency, concurrency, and critical-path latency.
    fig,ax=plt.subplots(figsize=(7.5,4.2))
    bars=[("A",0,2,3),("B",2,5,2),("D",2,3,1),("C",7,2,0)]
    for name,start,dur,yy in bars:
        col=C["gray"] if name=="D" else C["rust"]
        ax.barh(yy,dur,left=start,height=.55,color=col,alpha=.85)
        ax.text(start+dur/2,yy,f"{name}: {dur}",ha="center",va="center",color="white",weight="bold")
    ax.plot([2,2],[1.4,2.6],color=C["gray"],ls="--",lw=1)
    ax.plot([7,7],[.4,1.6],color=C["gray"],ls="--",lw=1)
    arrow(ax,(5,1),(7,1),"gray")
    ax.set(yticks=[0,1,2,3],yticklabels=["C","D","B","A"],
       xlim=(0,10),ylim=(-.8,3.8),xlabel=tr(lang,"Elapsed time (one consistent unit)","经过时间（同一单位）"))
    ax.set_xticks(range(11));ax.grid(axis="x",alpha=.18)
    ax.set_title(tr(lang,"A → {B, D in parallel} → C","A → {B、D并行} → C"),fontsize=12,pad=12)
    ax.text(.5,-.30,tr(lang,"Critical path: 2 + max(5, 3) + 2 = 9\nSum of all tasks: 12    Longest single task: 5",
       "关键路径：2 + max(5, 3) + 2 = 9\n全部工序相加：12    最长单项：5"),
       transform=ax.transAxes,ha="center",va="top",fontsize=11,color=C["ink"])
    fig.subplots_adjust(bottom=.30);save(fig,"critical-path",lang)

mf=ROOT/"_work/qa/mechanism-figures.json"
if len(sys.argv)>1 and mf.exists():
    prior=json.loads(mf.read_text(encoding="utf-8"))
    changed={(x["name"],x["language"]) for x in manifest}
    manifest=[x for x in prior if (x["name"],x["language"]) not in changed]+manifest
mf.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"new_figure_types":len(manifest)//2,"bilingual_assets":len(manifest)*3}))
