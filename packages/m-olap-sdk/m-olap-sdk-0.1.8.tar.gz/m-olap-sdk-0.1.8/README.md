OlapSDK
===============
module mining data in OLAP

Prepare
Đảm bảo rằng image phải được cài đặt mysql-devel, trong Dockerfile thêm dòng sau trước khi install requirements

```
RUN yum install -y gcc
RUN yum install -y python38-devel mysql-devel
RUN ln -s /usr/include/python3.8 /usr/local/include/python3.8
```

Usage

* Get profile by id
```python
from mobio.libs.olap.mining_warehouse.profiling.mysql_dialect.profiling_dialect import ProfilingDialect

profile_data = ProfilingDialect(olap_uri="uri").get_profile_by_criteria(merchant_id="merchant_id", profile_id="profile_id", lst_criteria=["cri_merchant_id", "cri_profile_id", "cri_name"])
print(profile_data)
```

Release notes:
* 0.1.4 (2023-11-28):
  * fix validate column name, support dynamic field with prefix
* 0.1.3 (2023-11-27):
  * remove m-utilities, chỉ dependence m-logging để support python3.8
* 0.1.2 (2023-11-27):
  * alter table
* 0.1.1 (2023-11-24):
  * support lấy profile by id, hỗ trợ việc masking data