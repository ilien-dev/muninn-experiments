# PM-Bench score report

## Summary

Hit: 33 | Late: 1 | Miss: 47 | False alarms: 3 | Commission: 0 | Wrong-content: 1 | Dependency violations: 0 | Overkill steps: 3 | state query calls: 1 | check_time calls: 1 | Actions: 37
Exact-set: matches 45 | mismatches 35 | reward 10
Set micro: TP 33 | FP 4 | FN 48
Cross-day: hit 1 | late 0 | miss 6 | total 7
Updates: hit 3 | late 0 | miss 6 | canceled 2 | total 11 | violations 0
Rates: hit 40.7% | late 1.2% | miss 58.0% | false alarm/step 3.8% | commission 0.0% | wrong-content 1.2% | dependency/step 0.0% | overkill/step 3.8% | cross-day miss 85.7% | update miss 66.7% | precision_hit 89.2% | precision_any 91.9% | exact-set match rate 56.2% | exact-set avg reward 0.125 | set_precision 89.2% | set_recall 40.7% | set_f1 55.9%
Hit rates (by modality): event 47.4% | time 25.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-13T09:35:42.681Z |
| Finished (UTC) | 2026-09-13T09:53:49.955Z |
| Duration | 18m 7.3s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 33 |
| Late | 1 |
| Miss | 47 |
| False alarms | 3 |
| Commission | 0 |
| Wrong-content | 1 |
| Dependency violations | 0 |
| Overkill steps | 3 |
| State query calls | 1 |
| Check_time calls | 1 |
| Actions | 37 |
| Exact-set matches | 45 |
| Exact-set mismatches | 35 |
| Exact-set reward | 10 |
| Set TP | 33 |
| Set FP | 4 |
| Set FN | 48 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| clock | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 40.7% |
| Late rate | 1.2% |
| Miss rate | 58.0% |
| False alarm/step | 3.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 1.2% |
| Dependency/step | 0.0% |
| Overkill/step | 3.8% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 66.7% |
| Precision hit | 89.2% |
| Precision any | 91.9% |
| Exact-set match rate | 56.2% |
| Exact-set avg reward | 0.125 |
| Set precision | 89.2% |
| Set recall | 40.7% |
| Set F1 | 55.9% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 27 | 57 | 47.4% |
| Time (time + time_check) | 6 | 24 | 25.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 27 | 0 | 15 | 42 | 64.3% | 64.3% |
| proactive_monitoring_required | 6 | 1 | 32 | 39 | 15.4% | 17.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 6 | 0 | 18 | 24 | 25.0% | 25.0% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 55.6% | 100.0% | 83.3% | 50.0% | 76.9% | 0.538 | 100.0% | 66.7% | 80.0% |
| Tuesday | 5 | 0 | 6 | 45.5% | 0.0% | 54.5% | 7.7% | 7.7% | 57.1% | 25.0% | 100.0% | 14.3% | 61.5% | 0.231 | 83.3% | 45.5% | 58.8% |
| Wednesday | 4 | 0 | 7 | 36.4% | 0.0% | 63.6% | 0.0% | 0.0% | 33.3% | 50.0% | 50.0% | 20.0% | 60.0% | 0.200 | 100.0% | 36.4% | 53.3% |
| Thursday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 0.0% | 0.0% | 77.8% | 0.0% | 87.5% | 0.0% | 72.7% | 0.455 | 100.0% | 58.3% | 73.7% |
| Friday | 1 | 1 | 10 | 8.3% | 8.3% | 83.3% | 8.3% | 8.3% | 12.5% | 0.0% | 16.7% | 0.0% | 33.3% | -0.333 | 33.3% | 8.3% | 13.3% |
| Saturday | 5 | 0 | 9 | 35.7% | 0.0% | 64.3% | 0.0% | 0.0% | 40.0% | 25.0% | 50.0% | 16.7% | 40.0% | -0.200 | 100.0% | 35.7% | 52.6% |
| Sunday | 3 | 0 | 6 | 33.3% | 0.0% | 66.7% | 9.1% | 9.1% | 60.0% | 0.0% | 75.0% | 0.0% | 45.5% | -0.091 | 75.0% | 33.3% | 46.2% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 1 |
| Tuesday | (none) | 0 |
| Wednesday | (none) | 0 |
| Thursday | (none) | 0 |
| Friday | (none) | 0 |
| Saturday | (none) | 0 |
| Sunday | (none) | 0 |
