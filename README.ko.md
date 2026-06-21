# StemCell Operator — Codex 앱 프로젝트 키트

이 키트는 생물학의 유전자 발현 개념을 Kubernetes Operator로 구현하기 위한 **Codex 앱 전용 개발 환경**입니다. 하나의 불변 OCI 이미지가 `api`, `worker`, `ai` 중 정확히 하나의 역할을 발현하며, 역할 전환은 실행 중 프로세스 변이가 아니라 Kubernetes의 선언적 롤아웃으로 수행됩니다.

## 권장 운영 모델

> **Cloud가 구현안을 만들고, Local Worktree가 Kubernetes 환경에서 증명합니다.**

| 실행 모드 | 권장 작업 | 단독으로 완료를 주장할 수 없는 항목 |
|---|---|---|
| Cloud | 스캐폴딩, Go 구현, 단위·envtest, 문서, 독립 리뷰 | 로컬 Docker, kind, 사설망·레지스트리 검증 |
| Worktree | Cloud 결과 통합, 격리된 병렬 개발, 충돌 해결 | 확인되지 않은 Kubernetes 컨텍스트 작업 |
| Local | 최종 통합과 의도적인 메인 체크아웃 수정 | 무인 장시간 작업의 기본 실행 위치 |
| App Automation | 항상 켜진 개발 머신의 반복 점검 | PC나 Codex 앱이 종료된 동안의 실행 |

이 저장소에는 Codex API 호출, `openai/codex-action`, `OPENAI_API_KEY` Secret, SMTP 알림 스크립트가 없습니다. Cloud task, Worktree, Automation, GitHub review는 Codex 앱·웹 설정에서 구성합니다.

## 포함된 구성

- `docs/SPEC.md`: 사용자, 기능 범위, API 계약, 성공 기준 `SC-01`~`SC-12`
- `AGENTS.md`, `Instructions.md`: Codex가 항상 따라야 하는 저장소 규칙
- `.agents/skills/`: 반복 작업을 위한 11개 프로젝트 Skill
- `.codex/agents/`: 아키텍트·구현·코드 리뷰·테스트·보안·배포 검증 에이전트 6개
- `prompts/cloud/`: M0~M4 구현, 독립 리뷰, 야간 배치용 Cloud 프롬프트
- `prompts/local/`: Cloud 결과 통합, kind E2E, 마일스톤 승인 프롬프트
- `prompts/automation/`: 전용 Worktree에서 실행하는 선택적 App Automation 프롬프트
- `scripts/`: Cloud setup, Worktree setup, 정적 검증, kubeconfig/kind 안전 게이트
- `.github/pull_request_template.md`: Cloud 증거와 `LOCAL_REQUIRED` 항목을 분리하는 PR 계약
- `.worktreeinclude`: ignored credential이 Worktree로 복사되지 않도록 기본 비어 있는 안전 설정

## 시작 순서

```bash
unzip stemcell-operator-codex-app-kit.zip
cd stemcell-operator-codex-app-kit
bash scripts/validate-repo.sh
```

이후 다음 순서로 진행합니다.

1. 키트 전체를 Git 저장소에 커밋하고 GitHub에 push합니다.
2. Codex Cloud에 저장소와 Cloud environment를 연결합니다.
3. Codex 앱에서 같은 저장소를 프로젝트로 엽니다.
4. `docs/CODEX_APP_SETUP.md`에 따라 Cloud setup script와 Worktree setup/action을 등록합니다.
5. Cloud에서 `prompts/cloud/01-m0-scaffold.md`를 실행합니다.
6. 결과 branch 또는 Draft PR을 Local Worktree에서 `prompts/local/01-integrate-cloud-change.md`로 통합합니다.
7. Docker와 kind가 준비된 로컬 환경에서 `prompts/local/02-kind-e2e.md`를 수행합니다.

## 첫 Cloud task

```text
Read AGENTS.md, Instructions.md, docs/SPEC.md, docs/ARCHITECTURE.md,
docs/BACKLOG.md, docs/OPERATING_MODEL.md, and
prompts/cloud/01-m0-scaffold.md.

Execution mode: Cloud.
Complete M0 only. Explicitly spawn the required custom agents.
Run bash scripts/verify-cloud.sh. Return a reviewable diff or Draft PR,
and mark Docker/kind work LOCAL_REQUIRED.
```

## 야간 작업

PC가 꺼질 수 있다면 한 에이전트에게 모호한 “6~8시간 작업”을 맡기지 않고, `prompts/cloud/07-overnight-batch.md`를 기준으로 파일 소유권이 겹치지 않는 Cloud task 3~5개를 시작합니다. 각 task는 완료 조건에 도달하면 diff, branch 또는 Draft PR과 `LOCAL_REQUIRED` 목록을 남깁니다. 다음 날 Local Worktree에서 하나씩 통합하고 kind 검증을 수행합니다.

Codex 앱 Automation은 로컬 실행입니다. 사용할 때는 전용 Worktree를 선택하고 PC와 앱을 켜 둡니다. 결과는 Codex 앱의 Triage inbox에서 확인하며, 이메일 완료 신호가 필요하면 Draft PR에 대한 GitHub 알림을 이용합니다.

## 검증

```bash
# 키트 구조, TOML, Skill, custom agent, shell/Python 구문 검사
bash scripts/validate-repo.sh

# Go/Kubebuilder 구현 이후 Cloud-safe 검증
bash scripts/verify-cloud.sh

# 구현 이후 외부 kubeconfig를 거부하고 isolated kind E2E 실행
unset KUBECONFIG
bash scripts/verify-local.sh
```

실제 Codex Cloud 및 kind 실행 전 설정은 `docs/CODEX_APP_SETUP.md`, 운영 경계는 `docs/OPERATING_MODEL.md`, 이전 API 키트에서의 변경 사항은 `docs/MIGRATION_FROM_API_KIT.md`를 확인합니다.
