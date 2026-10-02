# PM-Bench score report

## Summary

Hit: 54 | Late: 1 | Miss: 26 | False alarms: 13 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 11 | state query calls: 49 | check_time calls: 31 | Actions: 68
Exact-set: matches 52 | mismatches 32 | reward 20
Set micro: TP 54 | FP 14 | FN 27
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 1 | miss 1 | canceled 2 | total 11 | violations 2
Rates: hit 66.7% | late 1.2% | miss 32.1% | false alarm/step 15.5% | commission 0.0% | wrong-content 7.4% | dependency/step 0.0% | overkill/step 13.1% | cross-day miss 0.0% | update miss 11.1% | precision_hit 79.4% | precision_any 80.9% | exact-set match rate 61.9% | exact-set avg reward 0.238 | set_precision 79.4% | set_recall 66.7% | set_f1 72.5%
Hit rates (by modality): event 69.6% | time 60.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T07:05:30.000Z |
| Finished (UTC) | 2026-09-14T07:20:20.984Z |
| Duration | 14m 51.0s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 54 |
| Late | 1 |
| Miss | 26 |
| False alarms | 13 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 11 |
| State query calls | 49 |
| Check_time calls | 31 |
| Actions | 68 |
| Exact-set matches | 52 |
| Exact-set mismatches | 32 |
| Exact-set reward | 20 |
| Set TP | 54 |
| Set FP | 14 |
| Set FN | 27 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 3 |
| calendar | 1 |
| clock | 31 |
| course_portal | 6 |
| email | 1 |
| laundry_status | 1 |
| price_tracker | 2 |
| shipment_status | 4 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 66.7% |
| Late rate | 1.2% |
| Miss rate | 32.1% |
| False alarm/step | 15.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.4% |
| Dependency/step | 0.0% |
| Overkill/step | 13.1% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 79.4% |
| Precision any | 80.9% |
| Exact-set match rate | 61.9% |
| Exact-set avg reward | 0.238 |
| Set precision | 79.4% |
| Set recall | 66.7% |
| Set F1 | 72.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 56 | 69.6% |
| Time (time + time_check) | 15 | 25 | 60.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 15 | 1 | 25 | 41 | 36.6% | 39.0% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| calendar | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 15 | 1 | 9 | 25 | 60.0% | 64.0% |
| course_portal | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 4 | 4 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 15.4% | 15.4% | 80.0% | 75.0% | 100.0% | 60.0% | 76.9% | 0.538 | 77.8% | 77.8% | 77.8% |
| Tuesday | 8 | 1 | 3 | 66.7% | 8.3% | 25.0% | 0.0% | 9.1% | 75.0% | 50.0% | 100.0% | 33.3% | 63.6% | 0.273 | 88.9% | 66.7% | 76.2% |
| Wednesday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 28.6% | 14.3% | 60.0% | 50.0% | 75.0% | 40.0% | 71.4% | 0.429 | 55.6% | 55.6% | 55.6% |
| Thursday | 11 | 0 | 5 | 68.8% | 0.0% | 31.2% | 10.0% | 10.0% | 76.9% | 33.3% | 100.0% | 16.7% | 50.0% | 0.000 | 91.7% | 68.8% | 78.6% |
| Friday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 33.3% | 25.0% | 62.5% | 33.3% | 100.0% | 16.7% | 41.7% | -0.167 | 60.0% | 54.5% | 57.1% |
| Saturday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 62.5% | 100.0% | 100.0% | 57.1% | 75.0% | 0.500 | 100.0% | 75.0% | 85.7% |
| Sunday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 16.7% | 16.7% | 66.7% | 66.7% | 100.0% | 33.3% | 50.0% | 0.000 | 80.0% | 66.7% | 72.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 5 |
| Monday | email | 1 |
| Tuesday | clock | 4 |
| Tuesday | course_portal | 1 |
| Wednesday | appointment_portal | 3 |
| Wednesday | clock | 6 |
| Wednesday | shipment_status | 1 |
| Thursday | clock | 2 |
| Thursday | laundry_status | 1 |
| Thursday | price_tracker | 1 |
| Friday | calendar | 1 |
| Friday | clock | 3 |
| Friday | course_portal | 3 |
| Friday | price_tracker | 1 |
| Saturday | clock | 6 |
| Saturday | shipment_status | 3 |
| Sunday | clock | 5 |
| Sunday | course_portal | 2 |
