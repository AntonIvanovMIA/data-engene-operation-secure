# RBAC Implementation
**Author:** Mohammad Ali | **Week:** 5-6 | **Project:** Catnip Games International

## Overview
Implemented Role-Based Access Control in Elasticsearch to enforce
least-privilege access across all security log indices.

## Roles Created

### soc_analyst
| Property | Value |
|----------|-------|
| Purpose | Day-to-day monitoring and incident review |
| Cluster Privileges | monitor (read-only cluster stats) |
| Index Access | logstash-firewall-* READ only |
| Kibana Features | Discover, Dashboard, Visualise - read only |

### soc_engineer
| Property | Value |
|----------|-------|
| Purpose | Pipeline administration and full investigation |
| Cluster Privileges | monitor, manage_index_templates, manage_ilm, manage_pipeline |
| Index Access | logstash-firewall-* full read/write/manage |
| Kibana Features | All features including Dev Tools |

## Users Created
| Username | Role | Access Level |
|----------|------|-------------|
| analyst_user | soc_analyst | Read-only monitoring |
| engineer_user | soc_engineer | Full administrative |

## Design Rationale
Principle of least privilege applied. SOC analysts can investigate
events through dashboards but cannot modify Logstash pipelines,
delete indices, or access Dev Tools - preventing accidental changes
during live incident investigations.

## Verification
Run in Kibana Dev Tools:
GET /_security/role/soc_analyst
GET /_security/role/soc_engineer
GET /_security/user/analyst_user
GET /_security/user/engineer_user

## Licence Note
Field-level security requires an Enterprise licence.
Index-level and Kibana feature-level RBAC implemented
within Basic licence constraints.
