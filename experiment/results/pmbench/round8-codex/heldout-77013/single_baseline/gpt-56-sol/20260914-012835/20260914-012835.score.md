# PM-Bench score report

## Summary

Hit: 59 | Late: 0 | Miss: 22 | False alarms: 13 | Commission: 0 | Wrong-content: 7 | Dependency violations: 0 | Overkill steps: 10 | state query calls: 54 | check_time calls: 24 | Actions: 72
Exact-set: matches 55 | mismatches 29 | reward 26
Set micro: TP 59 | FP 13 | FN 22
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 1
Rates: hit 72.8% | late 0.0% | miss 27.2% | false alarm/step 15.5% | commission 0.0% | wrong-content 8.6% | dependency/step 0.0% | overkill/step 11.9% | cross-day miss 0.0% | update miss 22.2% | precision_hit 81.9% | precision_any 81.9% | exact-set match rate 65.5% | exact-set avg reward 0.310 | set_precision 81.9% | set_recall 72.8% | set_f1 77.1%
Hit rates (by modality): event 73.2% | time 72.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T07:28:35.214Z |
| Finished (UTC) | 2026-09-14T07:40:53.859Z |
| Duration | 12m 18.6s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 59 |
| Late | 0 |
| Miss | 22 |
| False alarms | 13 |
| Commission | 0 |
| Wrong-content | 7 |
| Dependency violations | 0 |
| Overkill steps | 10 |
| State query calls | 54 |
| Check_time calls | 24 |
| Actions | 72 |
| Exact-set matches | 55 |
| Exact-set mismatches | 29 |
| Exact-set reward | 26 |
| Set TP | 59 |
| Set FP | 13 |
| Set FN | 22 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 5 |
| bank_balance | 1 |
| calendar | 3 |
| clock | 24 |
| course_portal | 4 |
| email | 3 |
| laundry_status | 2 |
| library_hold | 2 |
| price_tracker | 4 |
| shipment_status | 6 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 72.8% |
| Late rate | 0.0% |
| Miss rate | 27.2% |
| False alarm/step | 15.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 8.6% |
| Dependency/step | 0.0% |
| Overkill/step | 11.9% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 22.2% |
| Precision hit | 81.9% |
| Precision any | 81.9% |
| Exact-set match rate | 65.5% |
| Exact-set avg reward | 0.310 |
| Set precision | 81.9% |
| Set recall | 72.8% |
| Set F1 | 77.1% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 41 | 56 | 73.2% |
| Time (time + time_check) | 18 | 25 | 72.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 20 | 0 | 21 | 41 | 48.8% | 48.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 18 | 0 | 7 | 25 | 72.0% | 72.0% |
| course_portal | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 1 | 0 | 3 | 4 | 25.0% | 25.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 15.4% | 15.4% | 80.0% | 75.0% | 100.0% | 60.0% | 76.9% | 0.538 | 77.8% | 77.8% | 77.8% |
| Tuesday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 18.2% | 18.2% | 75.0% | 75.0% | 100.0% | 50.0% | 63.6% | 0.273 | 81.8% | 75.0% | 78.3% |
| Wednesday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 21.4% | 7.1% | 60.0% | 75.0% | 75.0% | 60.0% | 71.4% | 0.429 | 66.7% | 66.7% | 66.7% |
| Thursday | 11 | 0 | 5 | 68.8% | 0.0% | 31.2% | 10.0% | 10.0% | 76.9% | 33.3% | 100.0% | 16.7% | 40.0% | -0.200 | 91.7% | 68.8% | 78.6% |
| Friday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 25.0% | 16.7% | 87.5% | 33.3% | 100.0% | 50.0% | 66.7% | 0.333 | 72.7% | 72.7% | 72.7% |
| Saturday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 62.5% | 100.0% | 100.0% | 57.1% | 75.0% | 0.500 | 100.0% | 75.0% | 85.7% |
| Sunday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 16.7% | 16.7% | 66.7% | 100.0% | 100.0% | 50.0% | 58.3% | 0.167 | 81.8% | 75.0% | 78.3% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 5 |
| Monday | email | 1 |
| Monday | shipment_status | 1 |
| Tuesday | appointment_portal | 2 |
| Tuesday | clock | 3 |
| Tuesday | email | 1 |
| Wednesday | appointment_portal | 3 |
| Wednesday | clock | 6 |
| Wednesday | email | 1 |
| Wednesday | shipment_status | 1 |
| Thursday | clock | 2 |
| Thursday | laundry_status | 1 |
| Thursday | price_tracker | 2 |
| Friday | calendar | 3 |
| Friday | clock | 1 |
| Friday | course_portal | 3 |
| Friday | price_tracker | 1 |
| Saturday | clock | 4 |
| Saturday | laundry_status | 1 |
| Saturday | price_tracker | 1 |
| Saturday | shipment_status | 4 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 3 |
| Sunday | course_portal | 1 |
| Sunday | library_hold | 2 |
