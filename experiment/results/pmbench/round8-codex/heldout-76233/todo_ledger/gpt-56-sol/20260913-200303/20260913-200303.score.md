# PM-Bench score report

## Summary

Hit: 57 | Late: 1 | Miss: 21 | False alarms: 10 | Commission: 0 | Wrong-content: 5 | Dependency violations: 0 | Overkill steps: 6 | state query calls: 42 | check_time calls: 28 | Actions: 68
Exact-set: matches 53 | mismatches 23 | reward 30
Set micro: TP 57 | FP 11 | FN 22
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 6 | late 1 | miss 2 | canceled 2 | total 11 | violations 3
Rates: hit 72.2% | late 1.3% | miss 26.6% | false alarm/step 13.2% | commission 0.0% | wrong-content 6.3% | dependency/step 0.0% | overkill/step 7.9% | cross-day miss 14.3% | update miss 22.2% | precision_hit 83.8% | precision_any 85.3% | exact-set match rate 69.7% | exact-set avg reward 0.395 | set_precision 83.8% | set_recall 72.2% | set_f1 77.6%
Hit rates (by modality): event 72.2% | time 72.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T02:03:03.476Z |
| Finished (UTC) | 2026-09-14T02:16:15.680Z |
| Duration | 13m 12.2s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 57 |
| Late | 1 |
| Miss | 21 |
| False alarms | 10 |
| Commission | 0 |
| Wrong-content | 5 |
| Dependency violations | 0 |
| Overkill steps | 6 |
| State query calls | 42 |
| Check_time calls | 28 |
| Actions | 68 |
| Exact-set matches | 53 |
| Exact-set mismatches | 23 |
| Exact-set reward | 30 |
| Set TP | 57 |
| Set FP | 11 |
| Set FN | 22 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 4 |
| bank_balance | 1 |
| calendar | 2 |
| clock | 28 |
| course_portal | 1 |
| email | 1 |
| laundry_status | 1 |
| price_tracker | 2 |
| shipment_status | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 72.2% |
| Late rate | 1.3% |
| Miss rate | 26.6% |
| False alarm/step | 13.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 6.3% |
| Dependency/step | 0.0% |
| Overkill/step | 7.9% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 22.2% |
| Precision hit | 83.8% |
| Precision any | 85.3% |
| Exact-set match rate | 69.7% |
| Exact-set avg reward | 0.395 |
| Set precision | 83.8% |
| Set recall | 72.2% |
| Set F1 | 77.6% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 54 | 72.2% |
| Time (time + time_check) | 18 | 25 | 72.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 18 | 1 | 20 | 39 | 46.2% | 48.7% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| clock | 18 | 1 | 6 | 25 | 72.0% | 76.0% |
| email | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 16.7% | 8.3% | 71.4% | 75.0% | 100.0% | 50.0% | 66.7% | 0.333 | 80.0% | 72.7% | 76.2% |
| Tuesday | 10 | 0 | 3 | 76.9% | 0.0% | 23.1% | 10.0% | 10.0% | 77.8% | 75.0% | 100.0% | 50.0% | 70.0% | 0.400 | 90.9% | 76.9% | 83.3% |
| Wednesday | 5 | 0 | 5 | 50.0% | 0.0% | 50.0% | 30.0% | 10.0% | 57.1% | 33.3% | 100.0% | 16.7% | 50.0% | 0.000 | 62.5% | 50.0% | 55.6% |
| Thursday | 8 | 0 | 5 | 61.5% | 0.0% | 38.5% | 22.2% | 11.1% | 66.7% | 50.0% | 85.7% | 33.3% | 44.4% | -0.111 | 80.0% | 61.5% | 69.6% |
| Friday | 7 | 1 | 2 | 70.0% | 10.0% | 20.0% | 0.0% | 10.0% | 66.7% | 75.0% | 100.0% | 50.0% | 70.0% | 0.400 | 87.5% | 70.0% | 77.8% |
| Saturday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 16.7% | 8.3% | 75.0% | 100.0% | 100.0% | 50.0% | 83.3% | 0.667 | 80.0% | 80.0% | 80.0% |
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
| Wednesday | clock | 4 |
| Wednesday | laundry_status | 1 |
| Wednesday | price_tracker | 1 |
| Thursday | clock | 4 |
| Friday | calendar | 1 |
| Friday | clock | 4 |
| Friday | price_tracker | 1 |
| Saturday | appointment_portal | 2 |
| Saturday | clock | 4 |
| Saturday | course_portal | 1 |
| Sunday | clock | 4 |
| Sunday | shipment_status | 2 |
