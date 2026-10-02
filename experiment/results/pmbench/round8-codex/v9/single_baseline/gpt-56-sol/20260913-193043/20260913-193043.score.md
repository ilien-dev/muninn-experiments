# PM-Bench score report

## Summary

Hit: 64 | Late: 4 | Miss: 13 | False alarms: 11 | Commission: 0 | Wrong-content: 9 | Dependency violations: 0 | Overkill steps: 11 | state query calls: 58 | check_time calls: 26 | Actions: 79
Exact-set: matches 54 | mismatches 26 | reward 28
Set micro: TP 64 | FP 15 | FN 17
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 8 | late 0 | miss 1 | canceled 2 | total 11 | violations 1
Rates: hit 79.0% | late 4.9% | miss 16.0% | false alarm/step 13.8% | commission 0.0% | wrong-content 11.1% | dependency/step 0.0% | overkill/step 13.8% | cross-day miss 14.3% | update miss 11.1% | precision_hit 81.0% | precision_any 86.1% | exact-set match rate 67.5% | exact-set avg reward 0.350 | set_precision 81.0% | set_recall 79.0% | set_f1 80.0%
Hit rates (by modality): event 75.4% | time 87.5%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:30:43.154Z |
| Finished (UTC) | 2026-09-14T01:43:13.832Z |
| Duration | 12m 30.7s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 64 |
| Late | 4 |
| Miss | 13 |
| False alarms | 11 |
| Commission | 0 |
| Wrong-content | 9 |
| Dependency violations | 0 |
| Overkill steps | 11 |
| State query calls | 58 |
| Check_time calls | 26 |
| Actions | 79 |
| Exact-set matches | 54 |
| Exact-set mismatches | 26 |
| Exact-set reward | 28 |
| Set TP | 64 |
| Set FP | 15 |
| Set FN | 17 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 3 |
| bank_balance | 5 |
| calendar | 4 |
| clock | 26 |
| course_portal | 3 |
| email | 8 |
| laundry_status | 1 |
| library_hold | 4 |
| shipment_status | 4 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 79.0% |
| Late rate | 4.9% |
| Miss rate | 16.0% |
| False alarm/step | 13.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 11.1% |
| Dependency/step | 0.0% |
| Overkill/step | 13.8% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 11.1% |
| Precision hit | 81.0% |
| Precision any | 86.1% |
| Exact-set match rate | 67.5% |
| Exact-set avg reward | 0.350 |
| Set precision | 81.0% |
| Set recall | 79.0% |
| Set F1 | 80.0% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 43 | 57 | 75.4% |
| Time (time + time_check) | 21 | 24 | 87.5% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 3 | 42 | 92.9% | 92.9% |
| proactive_monitoring_required | 25 | 4 | 10 | 39 | 64.1% | 74.4% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| calendar | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| clock | 21 | 1 | 2 | 24 | 87.5% | 91.7% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 2 | 1 | 0 | 3 | 66.7% | 100.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 15.4% | 7.7% | 77.8% | 100.0% | 100.0% | 66.7% | 76.9% | 0.538 | 83.3% | 83.3% | 83.3% |
| Tuesday | 9 | 1 | 1 | 81.8% | 9.1% | 9.1% | 7.7% | 15.4% | 71.4% | 100.0% | 100.0% | 71.4% | 69.2% | 0.385 | 81.8% | 81.8% | 81.8% |
| Wednesday | 8 | 1 | 2 | 72.7% | 9.1% | 18.2% | 10.0% | 10.0% | 77.8% | 50.0% | 100.0% | 40.0% | 60.0% | 0.200 | 80.0% | 72.7% | 76.2% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 18.2% | 18.2% | 77.8% | 66.7% | 87.5% | 50.0% | 63.6% | 0.273 | 81.8% | 75.0% | 78.3% |
| Friday | 8 | 2 | 2 | 66.7% | 16.7% | 16.7% | 16.7% | 16.7% | 50.0% | 100.0% | 66.7% | 66.7% | 58.3% | 0.167 | 66.7% | 66.7% | 66.7% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 30.0% | 30.0% | 80.0% | 75.0% | 100.0% | 50.0% | 40.0% | -0.200 | 78.6% | 78.6% | 78.6% |
| Sunday | 9 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 2 |
| Monday | clock | 3 |
| Monday | course_portal | 1 |
| Monday | email | 2 |
| Monday | library_hold | 1 |
| Tuesday | calendar | 2 |
| Tuesday | clock | 4 |
| Tuesday | email | 2 |
| Wednesday | bank_balance | 3 |
| Wednesday | clock | 2 |
| Wednesday | course_portal | 2 |
| Wednesday | library_hold | 2 |
| Thursday | clock | 3 |
| Thursday | shipment_status | 4 |
| Friday | clock | 5 |
| Friday | email | 4 |
| Friday | laundry_status | 1 |
| Friday | library_hold | 1 |
| Saturday | appointment_portal | 1 |
| Saturday | calendar | 2 |
| Saturday | clock | 4 |
| Sunday | bank_balance | 2 |
| Sunday | clock | 5 |
