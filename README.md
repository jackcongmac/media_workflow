# AI 古装短视频工作流实验

这个仓库用于设计和验证一套从选题研究到短视频发布的自动化工作流。

当前方向：

- 题材：皇帝、权力、古装、历史危机
- 形式：AI 古装电影感短剧
- 核心规则：成片必须是 moving video，不做 still image 连环画
- 第一阶段目标：先做 3 个风格测试，再决定是否进入 10 集第一季

## 文件

- `short_video_workflow_experiment.md`
  - 端到端工作流
  - 工具分工
  - 预算
  - 文件夹结构
  - 发布包规则

- `emperor_series_deep_research.md`
  - 皇帝系列是否值得做的研究简报
  - 题材机会和风险
  - 真人影视感、国画、连环画三种视觉路线比较
  - 下一步测试方案

## 当前结论

不要把项目做成历史科普，也不要做成静态图片推拉视频。

推荐定位：

**古装权力微短剧 / AI cinematic historical short drama**

第一轮测试：

1. 同一个脚本
2. 三个运动影像风格
3. 比较点击、完播、评论和主观吸引力

候选测试题：

- 秦始皇：焚书前夜
- 李世民：玄武门前夜
- 崇祯：最后一场朝会

## 克隆后继续

在另一台电脑上：

```bash
git clone https://github.com/jackcongmac/media_workflow.git
cd media_workflow
```

然后先读：

```bash
open short_video_workflow_experiment.md
open emperor_series_deep_research.md
```

下一步建议是先生成《焚书前夜》的 45-60 秒脚本，然后做三种 moving video 风格测试。
