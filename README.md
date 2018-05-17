# trafficPredict

## 项目组织
+ 初步设想将项目分为四个branch，分别为master，dataImport，dataAnalysis,trafficPredict.
+ 这样master里面放项目的整体文件，应该保证master总是可以运行的
+ dataImport目前由 `xUhEngwAng` 负责， 主要包括数据读入以及一些预处理
+ dataAnalysis 由 yufei 负责，涉及数据读入后的一些分析处理，拟合出各个变量之间的函数关系
+ trafficPredict 由 '火羽白' 负责，包括kalman滤波函数(或许另外放在一个branch里面)， 以及通过kalman滤波得出的交通流量预测值。

## 其他
+ 以后大家再慢慢补充一些细节进来，比如项目背景与说明之类的
+ 每次程序做了修改，测试通过后都 push 到这里，并且写清楚做的修改是什么，思路是什么
+ 每次工作前，都应该先在github看看其他人有无修改，如果有修改的话，先把修改pull到自己的本机上再在此基础上工作
+ 同济大学版权所有，转载需注明出处
