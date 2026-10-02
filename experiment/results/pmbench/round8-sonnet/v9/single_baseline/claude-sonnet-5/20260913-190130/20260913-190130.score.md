# PM-Bench score report

## Summary

Hit: 58 | Late: 2 | Miss: 21 | False alarms: 6 | Commission: 0 | Wrong-content: 1 | Dependency violations: 0 | Overkill steps: 7 | state query calls: 33 | check_time calls: 28 | Actions: 66
Exact-set: matches 53 | mismatches 27 | reward 26
Set micro: TP 58 | FP 8 | FN 23
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 1
Rates: hit 71.6% | late 2.5% | miss 25.9% | false alarm/step 7.5% | commission 0.0% | wrong-content 1.2% | dependency/step 0.0% | overkill/step 8.8% | cross-day miss 0.0% | update miss 22.2% | precision_hit 87.9% | precision_any 90.9% | exact-set match rate 66.2% | exact-set avg reward 0.325 | set_precision 87.9% | set_recall 71.6% | set_f1 78.9%
Hit rates (by modality): event 68.4% | time 79.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:01:30.320Z |
| Finished (UTC) | 2026-09-14T01:08:59.513Z |
| Duration | 7m 29.2s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 58 |
| Late | 2 |
| Miss | 21 |
| False alarms | 6 |
| Commission | 0 |
| Wrong-content | 1 |
| Dependency violations | 0 |
| Overkill steps | 7 |
| State query calls | 33 |
| Check_time calls | 28 |
| Actions | 66 |
| Exact-set matches | 53 |
| Exact-set mismatches | 27 |
| Exact-set reward | 26 |
| Set TP | 58 |
| Set FP | 8 |
| Set FN | 23 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 2 |
| clock | 28 |
| email | 3 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 71.6% |
| Late rate | 2.5% |
| Miss rate | 25.9% |
| False alarm/step | 7.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 1.2% |
| Dependency/step | 0.0% |
| Overkill/step | 8.8% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 22.2% |
| Precision hit | 87.9% |
| Precision any | 90.9% |
| Exact-set match rate | 66.2% |
| Exact-set avg reward | 0.325 |
| Set precision | 87.9% |
| Set recall | 71.6% |
| Set F1 | 78.9% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 57 | 68.4% |
| Time (time + time_check) | 19 | 24 | 79.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 3 | 42 | 92.9% | 92.9% |
| proactive_monitoring_required | 19 | 2 | 18 | 39 | 48.7% | 53.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 19 | 1 | 4 | 24 | 79.2% | 83.3% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 55.6% | 100.0% | 83.3% | 50.0% | 76.9% | 0.538 | 100.0% | 66.7% | 80.0% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 7.7% | 7.7% | 57.1% | 75.0% | 100.0% | 42.9% | 61.5% | 0.231 | 87.5% | 63.6% | 73.7% |
| Wednesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 10.0% | 10.0% | 66.7% | 50.0% | 100.0% | 20.0% | 60.0% | 0.200 | 87.5% | 63.6% | 73.7% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 18.2% | 18.2% | 77.8% | 66.7% | 87.5% | 50.0% | 63.6% | 0.273 | 81.8% | 75.0% | 78.3% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 10.0% | 10.0% | 80.0% | 75.0% | 100.0% | 50.0% | 60.0% | 0.200 | 91.7% | 78.6% | 84.6% |
| Sunday | 6 | 1 | 2 | 66.7% | 11.1% | 22.2% | 9.1% | 18.2% | 60.0% | 75.0% | 75.0% | 60.0% | 54.5% | 0.091 | 75.0% | 66.7% | 70.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 5 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 2 |
| Thursday | clock | 4 |
| Friday | clock | 5 |
| Friday | email | 3 |
| Saturday | clock | 4 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 5 |
