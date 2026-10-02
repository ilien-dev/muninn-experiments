# PM-Bench score report

## Summary

Hit: 60 | Late: 0 | Miss: 19 | False alarms: 10 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 7 | state query calls: 47 | check_time calls: 33 | Actions: 70
Exact-set: matches 54 | mismatches 22 | reward 32
Set micro: TP 60 | FP 10 | FN 19
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 0 | miss 1 | canceled 2 | total 11 | violations 1
Rates: hit 75.9% | late 0.0% | miss 24.1% | false alarm/step 13.2% | commission 0.0% | wrong-content 3.8% | dependency/step 0.0% | overkill/step 9.2% | cross-day miss 0.0% | update miss 11.1% | precision_hit 85.7% | precision_any 85.7% | exact-set match rate 71.1% | exact-set avg reward 0.421 | set_precision 85.7% | set_recall 75.9% | set_f1 80.5%
Hit rates (by modality): event 72.2% | time 84.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T02:16:17.173Z |
| Finished (UTC) | 2026-09-14T02:31:02.819Z |
| Duration | 14m 45.6s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 60 |
| Late | 0 |
| Miss | 19 |
| False alarms | 10 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 7 |
| State query calls | 47 |
| Check_time calls | 33 |
| Actions | 70 |
| Exact-set matches | 54 |
| Exact-set mismatches | 22 |
| Exact-set reward | 32 |
| Set TP | 60 |
| Set FP | 10 |
| Set FN | 19 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 4 |
| bank_balance | 1 |
| calendar | 2 |
| clock | 33 |
| course_portal | 1 |
| email | 2 |
| laundry_status | 1 |
| price_tracker | 1 |
| shipment_status | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 75.9% |
| Late rate | 0.0% |
| Miss rate | 24.1% |
| False alarm/step | 13.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 3.8% |
| Dependency/step | 0.0% |
| Overkill/step | 9.2% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 85.7% |
| Precision any | 85.7% |
| Exact-set match rate | 71.1% |
| Exact-set avg reward | 0.421 |
| Set precision | 85.7% |
| Set recall | 75.9% |
| Set F1 | 80.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 54 | 72.2% |
| Time (time + time_check) | 21 | 25 | 84.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 21 | 0 | 18 | 39 | 53.8% | 53.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| clock | 21 | 0 | 4 | 25 | 84.0% | 84.0% |
| email | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 16.7% | 16.7% | 71.4% | 75.0% | 100.0% | 50.0% | 58.3% | 0.167 | 80.0% | 72.7% | 76.2% |
| Tuesday | 11 | 0 | 2 | 84.6% | 0.0% | 15.4% | 0.0% | 0.0% | 77.8% | 100.0% | 100.0% | 66.7% | 90.0% | 0.800 | 100.0% | 84.6% | 91.7% |
| Wednesday | 5 | 0 | 5 | 50.0% | 0.0% | 50.0% | 40.0% | 20.0% | 57.1% | 33.3% | 100.0% | 16.7% | 50.0% | 0.000 | 55.6% | 50.0% | 52.6% |
| Thursday | 10 | 0 | 3 | 76.9% | 0.0% | 23.1% | 11.1% | 11.1% | 77.8% | 75.0% | 100.0% | 50.0% | 55.6% | 0.111 | 90.9% | 76.9% | 83.3% |
| Friday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 0.0% | 0.0% | 66.7% | 100.0% | 100.0% | 66.7% | 80.0% | 0.600 | 100.0% | 80.0% | 88.9% |
| Saturday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 25.0% | 16.7% | 62.5% | 100.0% | 83.3% | 50.0% | 66.7% | 0.333 | 70.0% | 70.0% | 70.0% |
| Sunday | 11 | 0 | 1 | 91.7% | 0.0% | 8.3% | 0.0% | 0.0% | 87.5% | 100.0% | 100.0% | 80.0% | 92.3% | 0.846 | 100.0% | 91.7% | 95.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 2 |
| Monday | bank_balance | 1 |
| Monday | clock | 4 |
| Tuesday | clock | 4 |
| Tuesday | email | 1 |
| Wednesday | calendar | 1 |
| Wednesday | clock | 5 |
| Wednesday | laundry_status | 1 |
| Thursday | clock | 5 |
| Friday | calendar | 1 |
| Friday | clock | 5 |
| Friday | price_tracker | 1 |
| Saturday | appointment_portal | 2 |
| Saturday | clock | 6 |
| Saturday | course_portal | 1 |
| Sunday | clock | 4 |
| Sunday | email | 1 |
| Sunday | shipment_status | 2 |
