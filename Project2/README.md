# Project2: implement the Rho method of reduced SM3
## 运行指导
直接在Python编译器中点击运行即可
## 代码说明
1. 依然先对SM3进行了实现
2. 通过改进的生日攻击，即The Rho method，可以降低存储空间，无需存储整个表格之后再作比较。

原理如下图所示：

相同hash值的两个碰撞，同时再hash相同次数后依然相同，因此会形成一个循环。

![](https://img-blog.csdnimg.cn/805e8622fbf64f99b12f79ecafba8f78.png)
![](https://img-blog.csdnimg.cn/b5119079c6594eeebbc848b8f2a29478.png)

随机选择一个x0之后，每hash一次的记为x1，hash两次的记为x2。设碰撞周期为T，那么当x1和x2相等时，它们之间相差周期的整数倍。如果想要找到什么时候开始进入循环的（即最早的碰撞），那么可以在0到i之间遍历找所有可能的周期。该种方法所用空间仅为O(1)，大大减少了生日攻击的消耗。

![](https://img-blog.csdnimg.cn/69dd3abc123d414e92da574815edc8af.png)

## 代码运行
分别控制n的值为8，16，24...均能快速得到结果

![](https://img-blog.csdnimg.cn/f0b9d8d7a92c4805beffc055595cde96.png)

![](https://img-blog.csdnimg.cn/5a8ec1a37c28441d8e0072699abfe211.png)

![](https://img-blog.csdnimg.cn/d848a2a3c390473b954de168dfb7b3a5.png)

可以看到，输出的碰撞均为256bit，这是因为除了x0以外，都已经经过了至少一次压缩，因此长度都是固定的256bit。
