# pywheel

Python项目的公共代码。


```bash
./scripts/publish.sh
```

### 安装

将发布到本地到包安装：

```bash
# 本地安装此库，将包发布到本地
/usr/local/bin/python3.10 setup.py install
```

安装本地库：

```bash
# 本地安装此库，将包发布到本地

```

```bash
# 打包
/usr/local/bin/python3.10 setup.py sdist bdist_wheel
# 上传
twine upload dist/*  --skip-existing          
```
