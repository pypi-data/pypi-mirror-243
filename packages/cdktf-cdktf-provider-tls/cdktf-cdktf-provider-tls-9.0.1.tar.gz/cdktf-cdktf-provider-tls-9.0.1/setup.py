import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-tls",
    "version": "9.0.1",
    "description": "Prebuilt tls Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-tls.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-tls.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_tls",
        "cdktf_cdktf_provider_tls._jsii",
        "cdktf_cdktf_provider_tls.cert_request",
        "cdktf_cdktf_provider_tls.data_tls_certificate",
        "cdktf_cdktf_provider_tls.data_tls_public_key",
        "cdktf_cdktf_provider_tls.locally_signed_cert",
        "cdktf_cdktf_provider_tls.private_key",
        "cdktf_cdktf_provider_tls.provider",
        "cdktf_cdktf_provider_tls.self_signed_cert"
    ],
    "package_data": {
        "cdktf_cdktf_provider_tls._jsii": [
            "provider-tls@9.0.1.jsii.tgz"
        ],
        "cdktf_cdktf_provider_tls": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "cdktf>=0.19.0, <0.20.0",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.92.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
