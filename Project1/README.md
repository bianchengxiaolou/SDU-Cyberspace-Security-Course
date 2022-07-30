# Project1: implement the naïve birthday attack of reduced SM3
## 运行指导
直接在Python编译器中点击运行即可
## 代码说明
1. 首先对SM3进行了实现，具体包含以下几个部分：
- 布尔函数

![](https://img-blog.csdnimg.cn/cd6ff035bfaf422ba902da242ea2f9eb.png)

- 置换函数

![](https://img-blog.csdnimg.cn/83452f7c13464fa68f93af0d6e806a1f.png)

- 消息扩展

![](https://img-blog.csdnimg.cn/050ad57cfcd94cbcbd6aa09420c9642e.png)

- 压缩过程

![](https://img-blog.csdnimg.cn/cf367c7a5e344b48bd2b69da5e3fdcac.png)

- 迭代过程

![](https://img-blog.csdnimg.cn/26b4724cbca541438310c2e2d6d6d732.png)


2. 随机生成两个消息，对它们进行SM3哈希。通过输入n可以选择取前面多少位来找碰撞。不断循环，当两个消息的哈希值的前n位相等时，输出这对碰撞。
3. 注：该CSDN账户是我本人，仅用于上传图片

![](https://img-blog.csdnimg.cn/8def4162127045c085ebfbc3fa46df35.png)

## 代码运行
1. 随机输入字符串，得到SM3哈希结果，可以看到花费时间较短，效率较高

![](https://img-blog.csdnimg.cn/a7e88efc57a94116a8c560376c54b60d.png)

2. 分别控制n的值为8，16，24...均能快速得到结果

![](https://img-blog.csdnimg.cn/48831f05a00f4ca5981783a3a0e190b6.png)

![](https://img-blog.csdnimg.cn/a9d46eaf5205460788e45d4bf9e8f32a.png)

![](https://img-blog.csdnimg.cn/c560c54e8a784fe8a3cb7f5d66bf6298.png)




- 部分参考：

        https://blog.csdn.net/weixin_43936250/article/details/105543266
        
        https://sca.gov.cn/sca/xwdt/2010-12/17/1002389/files/302a3ada057c4a73830536d03e683110.pdf
