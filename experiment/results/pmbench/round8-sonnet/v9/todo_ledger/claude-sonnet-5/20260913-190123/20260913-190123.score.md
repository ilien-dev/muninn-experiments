# PM-Bench score report

## Summary

Hit: 57 | Late: 2 | Miss: 22 | False alarms: 6 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 4 | state query calls: 27 | check_time calls: 24 | Actions: 65
Exact-set: matches 56 | mismatches 24 | reward 32
Set micro: TP 57 | FP 8 | FN 24
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 6 | late 1 | miss 2 | canceled 2 | total 11 | violations 3
Rates: hit 70.4% | late 2.5% | miss 27.2% | false alarm/step 7.5% | commission 0.0% | wrong-content 7.4% | dependency/step 0.0% | overkill/step 5.0% | cross-day miss 0.0% | update miss 22.2% | precision_hit 87.7% | precision_any 90.8% | exact-set match rate 70.0% | exact-set avg reward 0.400 | set_precision 87.7% | set_recall 70.4% | set_f1 78.1%
Hit rates (by modality): event 71.9% | time 66.7%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:01:23.820Z |
| Finished (UTC) | 2026-09-14T01:10:30.335Z |
| Duration | 9m 6.5s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 57 |
| Late | 2 |
| Miss | 22 |
| False alarms | 6 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 4 |
| State query calls | 27 |
| Check_time calls | 24 |
| Actions | 65 |
| Exact-set matches | 56 |
| Exact-set mismatches | 24 |
| Exact-set reward | 32 |
| Set TP | 57 |
| Set FP | 8 |
| Set FN | 24 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 1 |
| clock | 24 |
| email | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 70.4% |
| Late rate | 2.5% |
| Miss rate | 27.2% |
| False alarm/step | 7.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.4% |
| Dependency/step | 0.0% |
| Overkill/step | 5.0% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 22.2% |
| Precision hit | 87.7% |
| Precision any | 90.8% |
| Exact-set match rate | 70.0% |
| Exact-set avg reward | 0.400 |
| Set precision | 87.7% |
| Set recall | 70.4% |
| Set F1 | 78.1% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 41 | 57 | 71.9% |
| Time (time + time_check) | 16 | 24 | 66.7% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 41 | 0 | 1 | 42 | 97.6% | 97.6% |
| proactive_monitoring_required | 16 | 2 | 21 | 39 | 41.0% | 46.2% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 16 | 1 | 7 | 24 | 66.7% | 70.8% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 66.7% | 100.0% | 100.0% | 50.0% | 76.9% | 0.538 | 100.0% | 75.0% | 85.7% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 0.0% | 0.0% | 57.1% | 75.0% | 100.0% | 42.9% | 69.2% | 0.385 | 100.0% | 63.6% | 77.8% |
| Wednesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 10.0% | 10.0% | 66.7% | 50.0% | 100.0% | 20.0% | 60.0% | 0.200 | 87.5% | 63.6% | 73.7% |
| Thursday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 9.1% | 18.2% | 88.9% | 33.3% | 100.0% | 25.0% | 63.6% | 0.273 | 81.8% | 75.0% | 78.3% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 8 | 0 | 6 | 57.1% | 0.0% | 42.9% | 30.0% | 10.0% | 70.0% | 25.0% | 87.5% | 16.7% | 50.0% | 0.000 | 72.7% | 57.1% | 64.0% |
| Sunday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 9.1% | 0.0% | 80.0% | 75.0% | 100.0% | 60.0% | 81.8% | 0.636 | 87.5% | 77.8% | 82.4% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 3 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 2 |
| Thursday | clock | 4 |
| Friday | clock | 5 |
| Friday | email | 2 |
| Saturday | clock | 2 |
| Sunday | clock | 5 |
