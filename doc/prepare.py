from pathlib import Path

headers = {
    "README.md": """---
layout: home
title: 首页
nav_order: 0
permalink: /
---
""",
    "CN/quick_start.md": """---
layout: default
title: 快速体验
nav_order: 2
""",
    "CN/install.md": """---
layout: default
title: 安装
nav_order: 1
""",
    "CN/project/project.md": """---
layout: default
title: 进行标注
nav_order: 3
has_children: true
permalink: docs/labeling
""",
    "CN/project/semantic_segmentation.md": """---
layout: default
title: 语义分割标注
parent: 进行标注
nav_order: 5
""",
    "CN/project/interactive_segmentation.md": """---
layout: default
title: 交互式分割标注
parent: 进行标注
nav_order: 7
""",
    "CN/project/instance_segmentation.md": """---
layout: default
title: 实例分割标注
parent: 进行标注
nav_order: 6
""",
    "CN/project/detection.md": """---
layout: default
title: 目标检测标注
parent: 进行标注
nav_order: 3
""",
    "CN/project/detection_auto_label.md": """---
layout: default
title: 目标检测自动标注
parent: 进行标注
nav_order: 4
""",
    "CN/project/classification.md": """---
layout: default
title: 图像分类标注
parent: 进行标注
nav_order: 1
""",
    "CN/project/classification_auto_label.md": """---
layout: default
title: 图像分类自动标注
parent: 进行标注
nav_order: 2
""",
    "CN/training/training.md": """---
layout: default
title: 进行训练
nav_order: 4
has_children: true
permalink: docs/training
""",
    "CN/training/PdLabel_PdX.md": """---
layout: default
title: PaddleX 分类/检测/分割
parent: 进行训练
nav_order: 4
""",
    "CN/training/PdLabel_PdDet.md": """---
layout: default
title: PaddleDetection 道路标志检测
parent: 进行训练
nav_order: 2
""",
    "CN/training/PdLabel_PdClas.md": """---
layout: default
title: PaddleClas 花朵分类
parent: 进行训练
nav_order: 1
""",
    "CN/training/PdLabel_PdSeg.md": """---
layout: default
title: PaddleSeg 图像分割
parent: 进行训练
nav_order: 3
""",
}

HERE = Path(__file__).parent.absolute()
for name, header in headers.items():
    path = HERE / name
    print(path)
    content = path.read_text()
    content = content.replace(".md", ".html")
    if path != HERE / "README.md":
        header += f"permalink: {str(name).replace('.md', '.html')}\n---\n\n"
    content = header + content
    path.write_text(content)
