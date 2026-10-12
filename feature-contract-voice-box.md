# Feature contract: Voice box

## 1. Feature summary and sponsorship

| Feature name | Voice box — local speech output organ |
| :---- | :---- |
| **Colloquial / alternative names** | `voice_box`; Qbot's voice |
| **Requesting programme / grant** | Robot4Henry family learning project |
| **Business owner / contact point** | Dan — confirmed project owner |
| **Product owner** | Dan — confirmed |
| **Technical lead(s)** | Unassigned; delivery-team review needed |
| **Design lead** | Dan and Henry for voice choice — proposed |
| **Cost centre** | Not applicable — hobby project |
| **Target release / delivery date** | No date requested |
| **Contract status** | Draft |
| **Contract version / last updated** | 0.1 / 2026-10-12 |
| **Requester / contract author** | Dan / Codex draft |

## 2. Funding, capacity and delivery constraints

| Team | Capacity / PM | Funding period | Notes / constraints |
| :---- | :---- | :---- | :---- |
| Robot4Henry | Unknown | Ongoing | Local-only project; hardware spend is approximately £40–50 per month. |

No delivery capacity, timeline, or additional hardware budget has been confirmed. The voice must run on the brain computer's older CPU with 8 GB RAM and no GPU.

## 3. Problem statement and desired outcome

### 3.1 Problem

Qbot can generate text replies but cannot speak them aloud. This prevents a natural robot conversation and leaves later mouth animation and listening/speaking coordination without a speech-output source.

### 3.2 Desired outcome

Qbot can turn an appropriate reply into audible local speech through its speaker, using a voice Henry helps choose. Other code should be able to request, stop, and observe speech without knowing which speech engine or audio device is used.

### 3.3 Why now

This is the stated goal of R-307, a prerequisite for interruption handling (R-309) and part of the planned conversational head.

### 3.4 Evidence and current workaround

R-307 records local TTS, likely Piper, as the intended capability. The current workaround is reading terminal text. No voice shortlist, user testing, or hardware speaker evidence has yet been recorded.

## 4. Users, use cases and workflows

### 4.1 Primary users

Henry (7) and his sister (3) are the listeners; Dan supervises, selects/configures hardware, and approves child-facing behaviour.

### 4.2 Use cases

| ID | User need | Value / decision enabled | Priority |
| :---- | :---- | :---- | :---- |
| UC-01 | As a child, I need Qbot to say its reply aloud so that conversation feels like talking to a robot. | Core spoken interaction | Must |
| UC-02 | As Dan, I need to choose or replace the voice without changing callers of the organ. | A voice suitable for the family and future experimentation | Must |
| UC-03 | As the router, I need to know when speech starts and stops so that direction input can be muted and the mouth can animate. | Coordinates face and listening behaviour | Must |
| UC-04 | As a child, I need Qbot to stop speaking when interrupted. | Natural turn-taking | Should; delivery belongs with R-309 unless agreed otherwise |

### 4.3 End-to-end workflow

1. A future caller submits text chunks as the reply is generated.
2. The voice box produces speech locally and sends it to the selected audio output.
3. It exposes speaking state for the router; the router may mute direction and animate the mouth.
4. On completion, cancellation, unavailable voice engine, or unavailable audio output, the caller can observe the outcome and Qbot remains usable.

Representative normal input: the caller yields chunks that form “I found a fun fact about octopuses!” and Qbot starts speaking before the complete reply has arrived. Input is text chunks, not executable code or pre-generated audio.

### 4.4 Terminology

- **Voice box:** the `organs/voice_box/` boundary requested here; it produces sound but does not choose what Qbot says.
- **Synthesiser:** local software that converts text to audio, such as Piper.
- **Audio sink:** the speaker/output device that plays synthesised audio.
- **Streaming:** incremental input and/or incremental audible playback. Both need explicit definition.
- **Router:** the separate process that coordinates activity with eyes, mouth, lights, and direction (D-003/D-008).

## 5. Scope

### 5.1 In scope for this contract

- A separately pluggable `voice_box` organ interface.
- Local speech synthesis and playback for the selected initial engine/voice.
- Streamed text input, replacement cancellation, and observable speaking lifecycle.
- A fake or recording implementation for tests without audio hardware.

### 5.2 Explicitly out of scope

- Speech-to-text, microphone capture, wake/sleep behaviour, echo cancellation, and mouth firmware.
- Cloud speech services; the project is local-only.
- A final interruption/echo-cancellation solution; that is R-309.

### 5.3 Future extensions

- Streaming speech that begins before a whole LLM reply is ready.
- SSML/prosody controls, multiple voices/languages, sound effects, and mouth-viseme timing.
- Interruption and echo cancellation integrated with crown audio.

### 5.4 Assumptions

- The brain computer will have a usable speaker/audio-output path once R-306 is complete.
- A local CPU-capable voice engine can be selected after a shortlist and listening test.
- The future router owns face activity mapping, not `RobotBrain`.

## 6. Proposed solution and experience

### 6.1 Solution overview

**Proposal:** make `voice_box` a normal organ with an engine-independent request interface and pluggable local synthesis/playback implementations. It receives streamed text chunks and starts playback as soon as it has a speakable segment, without waiting for the complete LLM reply. A new request stops and replaces the current utterance.

Keep the public surface deliberately shallow: one operation to speak a stream, one cancellation operation on the returned request/handle, and a small set of lifecycle outcomes (`started`, `completed`, `cancelled`, `failed`). Segment buffering, synthesis, and audio-device details remain internal.

Candidate starting points, subject to delivery review:

| Option | Strength | Trade-off |
| :---- | :---- | :---- |
| Piper | Natural local neural voices; already named by R-307 | Model choice, packaging, and CPU latency need testing on the robot laptop |
| eSpeak NG | Tiny, offline, simple, robust fallback | Intentionally robotic quality may be less suitable for Qbot |
| Mimic 3 | Local neural alternative with a service/API model | Higher operational and resource complexity; suitability needs measurement |

Cloud TTS is excluded by the local-only project rule.

### 6.2 Entry points and navigation

There is no end-user screen. A future brain/voice orchestration caller submits speech; the router consumes lifecycle events or state. Dan needs a documented configuration point for voice and output device.

### 6.3 Interaction and display behaviour

| Area | Required behaviour | Notes / open detail |
| :---- | :---- | :---- |
| Input | Accept text chunks incrementally; buffer to sentence-ending punctuation where available, with a word/time fallback for an unpunctuated stream. | Exact fallback threshold is a delivery-team benchmark decision. |
| Playback | Play only locally through the configured output. | Speaker/device and volume behaviour are unknown. |
| Controls | A new speak request stops and replaces the current one; callers can observe cancellation, completion, and failure. | Pause/resume is out of scope. |
| Empty/error states | Empty input does not produce sound; engine/device failure does not crash Qbot. | Caller-facing error shape is a delivery-team question. |

### 6.4 Prototypes and designs

None yet. A voice-listening session with Henry is proposed once a shortlist runs on the robot laptop.

## 7. Functional requirements

| ID | User need / constraint | Requirement | Priority | Acceptance condition and evidence | Owner / confirmation |
| :---- | :---- | :---- | :---- | :---- | :---- |
| FR-01 | UC-01 | The system shall accept a stream of text chunks, form speakable segments at sentence boundaries with a word/time fallback, and turn them into audible local output. | Must | Given a chunked child-facing reply and configured speaker, Qbot begins audible playback before the final chunk arrives, without a network connection; a long unpunctuated stream also begins after the agreed fallback. | Dan; confirmed buffering rule 2026-10-12; threshold pending benchmark |
| FR-02 | UC-02 | The system shall isolate callers from the chosen synthesiser and audio sink. | Must | The same organ-level request passes against a recording fake and the selected real implementation. | Delivery team; proposed |
| FR-03 | UC-03 | The system shall expose start, completion, cancellation, and failure of an utterance. | Must | An automated test and manual demo show each lifecycle outcome; router integration remains a later dependency. | Delivery team; proposed |
| FR-04 | UC-03 | The system shall support one active utterance; a new request stops and replaces the current utterance. | Must | Given an active long utterance and a new request, the first reports `cancelled` and only the second continues audibly. | Dan; confirmed 2026-10-12 |
| FR-05 | UC-04 | The system should stop an active utterance promptly on cancellation. | Should | Given a long utterance and a cancellation request, no further audio is emitted within an agreed target. | Delivery team; target pending |

## 8. Non-functional requirements

| Category | Requirement / target | How verified |
| :---- | :---- | :---- |
| Performance | Measure time from first suitable text chunk to first audio, and total synthesis time, on the robot laptop using short and long child-facing replies. No numeric target agreed. | Recorded benchmark during voice shortlist. |
| Reliability | Engine or speaker failure must leave the main conversation process usable and report a clear outcome. | Automated fault-injection test. |
| Security / privacy | Speech text and generated audio remain on the robot computer; no cloud service is required. | Dependency/configuration review and offline demonstration. |
| Device support | Initial target is the brain computer's Linux audio output. | Manual playback test on robot hardware. |
| Observability | Log request lifecycle and non-sensitive failure reason; do not add unnecessary child transcript duplication. | Automated test and log review. |

## 9. Data contract

### 9.1 Inputs and ownership

| Data product / service | Format / interface | Owning team | Receiving / consuming team(s) | Owner responsibilities | Handover / validation |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Speech input | Ordered stream of text chunks | Future brain/voice caller | Voice box | Supply child-safe text according to the agreed contract | Validate type, emptiness, ordering, size, and cancellation semantics |
| Local voice model | Engine-specific local model file | Dan / delivery implementation | Voice box | Select and install a permitted offline voice | Verify version, licence, and robot-laptop performance |
| Audio device | Linux output device | Dan / hardware build | Voice box | Provide configured speaker path | Playback self-test |

### 9.2 Metadata and identifiers

Not applicable — this feature has no biological dataset. Delivery review should define only the minimum request metadata, likely request ID, voice selection, and source/caller context if needed for lifecycle correlation.

### 9.3 Data availability and failure behaviour

| Condition | Required behaviour | Owning team |
| :---- | :---- | :---- |
| Empty speech input | Produce no sound and report a non-error no-op. | Voice box |
| Missing voice model / engine | Report failure; do not crash the caller or fall back to cloud. | Voice box |
| Audio output unavailable | Report failure; preserve text interaction. | Voice box / hardware owner |
| Cancellation | Stop output according to the agreed policy and report cancellation. | Voice box |

### 9.4 Data lifecycle

Speech input is created by a future caller, validated and synthesised locally, played locally, and discarded unless minimal lifecycle telemetry is retained for debugging. Voice-model installation, updates, licence review, and removal need a delivery-team operating proposal.

## 10. Technical boundaries and dependencies

| Dependency / boundary | Why needed | Owner | Required by | Status / fallback |
| :---- | :---- | :---- | :---- | :---- |
| R-306 speaker/amplifier | Physical audible output | Dan / hardware work | Real-hardware acceptance | Planned; recording fake permits software work first |
| R-207 router | Talking state drives mouth/direction behaviour | Delivery team | Full face integration | Planned |
| R-307 | Project roadmap item this contract refines | Dan | Feature delivery | Planned |
| Local TTS engine and voice | Synthesis | Delivery team / Dan selects voice | Implementation | Piper proposed; eSpeak NG fallback to assess |

### 10.1 Architectural decisions

| Decision | Rationale | Alternatives considered | Date / owner |
| :---- | :---- | :---- | :---- |
| Speech is local to the brain computer | Project rule: no cloud; R-307 explicitly requests local TTS | Cloud TTS excluded | Confirmed by project documentation |
| Router receives activity, not voice-box-specific facial commands | D-008 assigns face mapping to router | Direct brain/organ coupling | Confirmed by D-008 |
| Organ boundary should be pluggable | Requester asks to plug it into later consumers | Direct engine use by callers | Requester direction; detailed interface pending review |

## 11. Delivery plan and milestones

| Milestone | Deliverable | Owner(s) | Target | Exit criteria |
| :---- | :---- | :---- | :---- | :---- |
| M1 | Confirmed feature contract | Dan | No date | Requester decisions in section 12 resolved or deliberately deferred |
| M2 | Engine/voice shortlist on robot laptop | Delivery team and Dan/Henry | No date | Measured local playback and a preferred voice recorded |
| M3 | Standalone organ with fake and real implementation | Delivery team | No date | FR-01 to FR-04 pass without router integration |
| M4 | Router coordination | Delivery team | Depends on R-207/R-306 | Talking state visibly coordinates output hardware |

### 11.1 Rollout approach

Begin with manual, supervised terminal playback using a recording fake in tests. Enable real output only after the selected speaker and voice have been tested with Dan present. No production rollout or feature flag has been defined.

### 11.2 Operational ownership and adoption

Dan is the proposed owner for voice selection, speaker configuration, and approval of child-facing sound. Delivery-team ownership for software maintenance is unassigned.

## 12. Risks, unknowns and decisions needed

| ID | Risk / open question | Impact / what it blocks | Owner / role to consult | Next action / decision needed by | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| V-01 | Resolved: input is streamed text chunks, not code or pre-generated audio. | Establishes the organ's input contract. | Dan | Recorded in sections 4, 6, 7, and 9. | Resolved 2026-10-12 |
| V-02 | Resolved: speech should begin before the complete reply is ready. | Requires incremental buffering/synthesis rather than whole-utterance-only playback. | Dan | Delivery team to assess engine support and benchmark it. | Resolved 2026-10-12 |
| V-03 | Resolved: a new utterance stops and replaces the current one; retain a shallow public interface. | Establishes single-active-utterance and cancellation semantics. | Dan | Delivery team to propose the minimal API. | Resolved 2026-10-12 |
| V-07 | Resolved: form segments at sentence-ending punctuation, with a word/time fallback for a long unpunctuated stream. | Defines natural incremental speech without indefinite waiting. | Dan | Delivery team to benchmark and propose the threshold on the robot laptop. | Resolved 2026-10-12 |
| V-04 | What hardware/audio path and volume controls will be used? | Blocks real-hardware acceptance, but not fake/engine work. | Dan / R-306 | Confirm when speaker plan is ready. | Open |
| V-05 | Which voice should Qbot use and what tone is suitable? | Blocks final voice selection, not interface work. | Henry and Dan | Shortlist after robot-laptop test. | Open |
| V-06 | Can the selected local engine meet acceptable latency on the robot laptop? | May change engine or scope. | Delivery team | Benchmark representative utterances locally. | Open |

## 13. Acceptance and success

### 13.1 Definition of done

- [ ] All Must functional requirements pass
- [ ] Non-functional targets have been measured and accepted
- [ ] Data contract and operational ownership are agreed
- [ ] UX/design review completed
- [ ] Accessibility review completed
- [ ] Documentation and support materials completed
- [ ] Product owner has accepted the release

### 13.2 User and product success measures

| Measure | Baseline / current evidence | Target / indicator | How measured | Owner / review timing |
| :---- | :---- | :---- | :---- | :---- |
| Audible conversational reply | Current baseline: terminal text only | Henry and Dan can complete a supervised spoken exchange with Qbot | Manual observation and feedback | Dan, after first hardware demo |
| Voice suitability | No shortlist yet | Henry can choose a voice he likes from locally tested options | Listening session | Dan and Henry, after M2 |
| Resilience | No voice output yet | A missing engine/speaker does not terminate text conversation | Automated fault test | Delivery team, before M3 acceptance |

### 13.3 Acceptance sign-off

| Role | Name | Decision | Date | Comments |
| :---- | :---- | :---- | :---- | :---- |
| Business / product owner | Dan | Pending |  |  |
| Technical lead | Unassigned | Pending |  |  |
| Design lead | Dan / Henry proposed | Pending |  |  |
| Data owner | Not applicable | Not applicable |  |  |

### 13.4 Requester handover readiness

| Check | Assessment / evidence or remaining gap |
| :---- | :---- |
| Problem, users and desired outcome are clear | Core outcome is clear: Qbot should speak locally. |
| Scope, exclusions and priorities are explicit | Core input, streaming, replacement, and buffering decisions are explicit. |
| Must requirements trace to needs and have observable acceptance conditions | Yes; numeric performance and buffering thresholds remain technical-review targets, not requester gaps. |
| Material data needs, constraints and dependencies are identified | Local-only rule, R-306, R-207, and R-307 are recorded. |
| Assumptions, unconfirmed commitments and team-review questions are visible | V-01 to V-06 identify unresolved requester and delivery questions. |
| Requester has reviewed the contract for faithful intent | Pending Dan's response. |

**Readiness assessment:** Ready for team review with open questions.

**Material remaining questions:** Voice choice and hardware path are dependencies; engine suitability, buffering thresholds, and a minimal API need delivery-team review. They do not obscure the requested user experience.

## 14. References and change history

### 14.1 Associated documents

| Source | Relevant section / version / date | What it supports |
| :---- | :---- | :---- |
| `docs/roadmap/items/programming/R-307-text-to-speech-and-qbot-s-voice.md` | 2026-10-08 | Local TTS, a voice Henry picks, and router talking state. |
| `docs/roadmap/items/physical/R-306-speaker-amplifier-and-enclosure.md` | Current roadmap | Speaker hardware dependency. |
| `docs/roadmap/items/programming/R-309-interruptions.md` | Current roadmap | Future interruption and echo-cancellation scope. |
| `docs/decisions/D-003-brain-computer-is-the-hub.md` | Accepted 2026-10-08 | Router is separate from chat and mutes direction while Qbot speaks. |
| `docs/decisions/D-008-brain-sends-mood-router-composes-face.md` | Accepted 2026-10-08 | Router owns face activity mapping. |
| `CLAUDE.md` | Project conventions | Local-only operation, hardware constraints, and child-facing expectations. |

### 14.2 Change log

| Version | Date | Author | Summary |
| :---- | :---- | :---- | :---- |
| 0.1 | 2026-10-12 | Codex | Initial requester-preparation draft based on R-307 and project decisions. |
| 0.2 | 2026-10-12 | Codex | Recorded streamed-text input, early playback, and stop-and-replace decisions. |
| 0.3 | 2026-10-12 | Codex | Recorded punctuation-first buffering with a word/time fallback; marked ready for team review with open technical questions. |
