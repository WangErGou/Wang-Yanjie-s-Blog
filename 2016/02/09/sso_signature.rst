基于SAML的单点登录系统 二
=========================


.. author:: default
.. categories:: 技术
.. tags:: SSO, Encryption, Signature
.. comments::

前言
----

刚接触的时候，对加密、签名这一块基本没什么了解，所以看的东西杂了一点。

写到最后，发现写具体的处理细节的话，是一件很没意思也很困难的事情，所以就把这部分省去了。


数据的加密方法
--------------

数据在传输的过程中，主要存在三种安全隐患：

    - 数据是否被偷读了？
    - 数据是否被修改了？
    - 是否有人伪造了身份？

为了解决这几个问题，机智如人类，想出了 **加密** 这个手段来保证：只有有权限读取数据的人才能依靠 **密钥** 来读取数据。

根据使用的密钥的不同，可以把加密方式分为 **Symmetric key encryption** 和 **Asymmetric key encryption** 两种。

如字面意，Symmetric key encryption 使用相同的密钥来加密和解密数据。
数据的发送者和接收者拥有一把相同的密钥。
数据在发送之前用密钥加密，随后将加密的数据发送出去。
接收者收到加密的数据后，使用相同的密钥来解密，得到数据。

而在 Asymmetric key encryption 中，存在两把不同但相关的密钥：私钥（private key）和公钥（public key）。
依然按字面意来理解，私钥是只有“自己”拥有的，而公钥是公开的。
根据加密目的的不同，可以将 Asymmetric key encryption 进一步细分，其中常见的两种是： **Public key encryption** 和 **Digit signatures** 。
在 Public key encryption 中，任何人都可以通过公钥来加密数据，而只有拥有私钥的人，才能读取数据。
在 Digit signatures 中，拥有私钥的人来加密数据，任何拥有公钥的人，都可以读取数据。
当然，在实际使用 Asymmetric key encryption 的过程中，一般还需要一个叫做 certificate authority(CA) 的角色。
CA 是一个 **trusted third party** ——同时被数据的发送和接收方所信任的组织。
CA 有权发布 **digit certififcate** 用于公证某个 publick key 的所有者信息。

Symmetric key encryption 看上去全部解决了三个安全隐患，但是因为数据的发送者和接收者拥有相同密钥，也导致了许多问题。
而 Public key encryption 和 Digit signatures 分别解决了三个安全隐患中的前两点和后两点。


SAML 签名
---------

SAML 没有规定具体的签名方法而是采用了 XML 规定的签名语法和流程，所以与其说 SAML 签名方法，不如说 XML 签名方法更贴切。

生成签名
++++++++

生成签名的过程可以分解成以下几步：

    1. 对每个需要签名的 XML 节点计算摘要

       - 按照 `Transforms` 指定的方法对节点进行转化
       - 计算格式化后的内容的摘要，生成 `DigestValue`
       - 生成 `Reference` 节点
    2. 生成 `SignedInfo` 节点

       - 包括所有 `Referece` 节点
       - 通过 `CanonicalizationMethod` 指定格式化方法
       - 通过 `SignatureMethod` 指定签名方法
    3. 计算 `SignedInfo` 节点的签名并生成 `SignatureValue` 节点

       - 按其指定的格式化方法对其内容进行格式化
       - 按其指定的签名方法，计算其签名，生成 `SignatureValue` 节点
    4. 生成最终的 `Signature` 节点

验证签名
++++++++

验证签名的过程可以分解成如下几步：

    1. 验证 `SignedInfo` 节点

       - 从 `KeyInfo` 节点或其他地方读取密钥
       - 根据 `CanonincalizationMethod` 指定的方法对 `SignedInfo` 进行格式化
       - 根据 `SignatureMethod` 指定的方法，用之前得到的密钥计算格式化后的内容的签名
       - 比较 1.3 中计算的签名和 `SignatureValue` 中的内容是否一致
    2. 验证每个 `Reference` 节点

       - 找到 `Reference` 对应的节点
       - 根据 `Transforms` 指定的方法对节点内容进行转换
       - 根据 `DigestMethod` 指定的方法提取转换后的内容的摘要
       - 比较计算得到的摘要和 `DigestMethod` 中的内容是否一致


参考文献
--------

#. `Encryption - Wikipedia, the free encyclopedia <https://en.wikipedia.org/wiki/Encryption>`_
#. `Public-key cryptography - Wikipedia, the free encyclopedia <https://en.wikipedia.org/wiki/Public-key_cryptography>`_
#. `XML Signature Syntax and Processing (Second Edition) <https://www.w3.org/TR/xmldsig-core/>`_
