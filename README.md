# CNN-captcha-recognition-for-Luogu

## 使用

1. 首先，确保你有 [TamperMonkey](https://www.tampermonkey.net/) 插件。
2. 下载上面的 [user.js](./user.js) 。
3. 在浏览器的右上角找到扩展——篡改猴——添加脚本。
4. 删除原有内容，将user.js拖到网页的编辑器中。
5. ctrl + s 保存。
6. ~~在本地运行 [app.py](./app.py)。什么？服务器？以后再说...~~
   (已经不需要这一步啦)


## 介绍
自动识别并填写洛谷提交时的验证码

简单的深度学习课程作业任务

最终测试集准确率在83%左右

~~(买不起服务器所以只好部署在本地了)~~
感谢 [同学](https://github.com/Hanserneko) 的支援,已经在服务器部署了

## 数据集
数据集全部来自https://github.com/langningchen/luoguCaptcha/tree/main/data

非常感谢大佬的数据集，当我在一片茫茫大海中到处寻找数据集的时候，他仓库的出现仿佛黑暗中的一道光

## 网络结构

非常经典的卷积池化三层结构

  1. 三层卷积 + 池化
  2. 展平 + 全连接
  3. 四路输出头

| 层      | 类型                        | 输出                 | 参数量                     |
| ------- | --------------------------- | -------------------- | -------------------------- |
| conv1   | Conv2d(3→32, k=3, p=1)      | (B, 32, 35, 90)      | 3×32×3×3 + 32 = 896        |
| pool1   | MaxPool2d(2×2)              | (B, 32, 17, 45)      | 0                          |
| conv2   | Conv2d(32→64, k=3, p=1)     | (B, 64, 17, 45)      | 32×64×3×3 + 64 = 18,496    |
| pool2   | MaxPool2d(2×2)              | (B, 64, 8, 22)       | 0                          |
| conv3   | Conv2d(64→128, k=3, p=1)    | (B, 128, 8, 22)      | 64×128×3×3 + 128 = 73,856  |
| pool3   | MaxPool2d(2×2)              | (B, 128, 4, 11)      | 0                          |
| flatten | —                           | (B, 5632)            | 0                          |
| fc      | Linear(5632→512)            | (B, 512)             | 5632×512 + 512 = 2,883,968 |
| head0–3 | Linear(512→NUM\_CLASSES) ×4 | (B, NUM\_CLASSES) ×4 | 4 × (512×C + C)            |



## Loss and Accuracy

![alt text](plt/loss.png)
![alt text](plt/acc.png)