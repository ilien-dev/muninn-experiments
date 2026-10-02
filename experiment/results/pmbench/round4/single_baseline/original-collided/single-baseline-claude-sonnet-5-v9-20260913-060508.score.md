# PM-Bench score report

## Summary

Hit: 59 | Late: 2 | Miss: 20 | False alarms: 6 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 6 | state query calls: 36 | check_time calls: 30 | Actions: 67
Exact-set: matches 56 | mismatches 24 | reward 32
Set micro: TP 59 | FP 8 | FN 22
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 5 | late 0 | miss 4 | canceled 2 | total 11 | violations 1
Rates: hit 72.8% | late 2.5% | miss 24.7% | false alarm/step 7.5% | commission 0.0% | wrong-content 3.7% | dependency/step 0.0% | overkill/step 7.5% | cross-day miss 0.0% | update miss 44.4% | precision_hit 88.1% | precision_any 91.0% | exact-set match rate 70.0% | exact-set avg reward 0.400 | set_precision 88.1% | set_recall 72.8% | set_f1 79.7%
Hit rates (by modality): event 71.9% | time 75.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-13T12:05:08.922Z |
| Finished (UTC) | 2026-09-13T12:47:13.264Z |
| Duration | 42m 4.3s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 59 |
| Late | 2 |
| Miss | 20 |
| False alarms | 6 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 6 |
| State query calls | 36 |
| Check_time calls | 30 |
| Actions | 67 |
| Exact-set matches | 56 |
| Exact-set mismatches | 24 |
| Exact-set reward | 32 |
| Set TP | 59 |
| Set FP | 8 |
| Set FN | 22 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 2 |
| clock | 30 |
| email | 3 |
| library_hold | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 72.8% |
| Late rate | 2.5% |
| Miss rate | 24.7% |
| False alarm/step | 7.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 3.7% |
| Dependency/step | 0.0% |
| Overkill/step | 7.5% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 44.4% |
| Precision hit | 88.1% |
| Precision any | 91.0% |
| Exact-set match rate | 70.0% |
| Exact-set avg reward | 0.400 |
| Set precision | 88.1% |
| Set recall | 72.8% |
| Set F1 | 79.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 41 | 57 | 71.9% |
| Time (time + time_check) | 18 | 24 | 75.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 40 | 0 | 2 | 42 | 95.2% | 95.2% |
| proactive_monitoring_required | 19 | 2 | 18 | 39 | 48.7% | 53.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 18 | 0 | 6 | 24 | 75.0% | 75.0% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 55.6% | 100.0% | 83.3% | 50.0% | 76.9% | 0.538 | 100.0% | 66.7% | 80.0% |
| Tuesday | 7 | 1 | 3 | 63.6% | 9.1% | 27.3% | 15.4% | 15.4% | 57.1% | 75.0% | 100.0% | 42.9% | 53.8% | 0.077 | 70.0% | 63.6% | 66.7% |
| Wednesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 10.0% | 10.0% | 66.7% | 50.0% | 100.0% | 20.0% | 60.0% | 0.200 | 87.5% | 63.6% | 73.7% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 9.1% | 9.1% | 88.9% | 33.3% | 100.0% | 25.0% | 72.7% | 0.455 | 90.0% | 75.0% | 81.8% |
| Friday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 0.0% | 0.0% | 62.5% | 100.0% | 83.3% | 66.7% | 83.3% | 0.667 | 90.0% | 75.0% | 81.8% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 10.0% | 10.0% | 80.0% | 75.0% | 100.0% | 50.0% | 60.0% | 0.200 | 91.7% | 78.6% | 84.6% |
| Sunday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 9.1% | 9.1% | 100.0% | 75.0% | 100.0% | 80.0% | 81.8% | 0.636 | 88.9% | 88.9% | 88.9% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 6 |
| Tuesday | email | 1 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 2 |
| Thursday | clock | 6 |
| Friday | clock | 6 |
| Friday | email | 2 |
| Friday | library_hold | 1 |
| Saturday | clock | 2 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 5 |
