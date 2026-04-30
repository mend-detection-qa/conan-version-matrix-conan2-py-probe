# conan2-py-python-requires

Probe targeting pattern `conan2-py-python-requires`: a Conan 2.x `conanfile.py` that exercises
`tool_requires` (and optionally `python_requires`) declared via the Conan 2.x Python API
(`from conan import ConanFile`). The probe uses a distinct package set — `zlib/1.3.1` and
`bzip2/1.0.8` as runtime dependencies, with `cmake/3.27.9` and `ninja/1.12.1` as build-time
tools — differentiating it from other tool_requires probes that use `poco`.

## Feature exercised

`tool_requires` declared inside `conanfile.py` using the Conan 2.x API. Both `cmake/3.27.9`
and `ninja/1.12.1` land in the lockfile's `build_requires` list. Mend must read `conan.lock`
and exclude every `build_requires` entry from the reported runtime dependency tree. Only the
two packages in the `requires` list (`zlib`, `bzip2`) must appear.

### python_requires — coverage note

`python_requires` was the original target feature for this probe. However, `cmake-conan` (the
canonical Conan Center recipe that exposes a helper class via `python_requires`) is no longer
published on Conan Center Index v2. No other package on Conan Center v2 is designed to be
consumed as a `python_requires` helper.

Consequence: the `python_requires` array in `conan.lock` is empty (`[]`). This is the correct
real-world resolution. The probe exercises the invariant from the other side: Mend must not
treat an empty `python_requires` array as an error, and must not surface any phantom
`python_requires` entries in the tree.

resolver knowledge: not available (no Conan UA resolver file in knowledge cache — tree is
exploratory).

## Expected dependency tree

### Direct runtime dependencies — MUST appear in Mend tree

| Package | Version | Lockfile key | Source |
|---------|---------|--------------|--------|
| zlib | 1.3.1 | requires | Conan Center (registry) |
| bzip2 | 1.0.8 | requires | Conan Center (registry) |

Both packages are leaf nodes: `zlib` and `bzip2` have no transitive runtime dependencies that
Conan resolves at this profile (Linux/gcc/Release/x86_64).

### Build-time dependencies — MUST NOT appear in Mend tree

| Package | Version | Lockfile key | Reason excluded |
|---------|---------|--------------|-----------------|
| cmake | 3.27.9 | build_requires | declared under `tool_requires` in conanfile.py |
| ninja | 1.12.1 | build_requires | declared under `tool_requires` in conanfile.py |

### python_requires — MUST NOT appear in Mend tree

| Entry | Value | Reason |
|-------|-------|--------|
| python_requires | [] (empty) | No Conan Center package available for python_requires; array is empty — Mend must not fabricate entries |

## Dependency types

- Runtime: `requires` — 2 packages, both direct, both leaf nodes.
- Build-time: `build_requires` — 2 entries (cmake/3.27.9, ninja/1.12.1); excluded from Mend tree.
- `python_requires`: empty list — Mend must tolerate this without error.
- `config_requires`: empty list.

## Probe metadata

- pattern: conan2-py-python-requires
- pm: conan
- conan_version: 2.28.1
- conanfile_type: conanfile.py (Conan 2.x `from conan import ConanFile`)
- schema_version: "1.0"
- lockfile: conan.lock (Conan 2.x flat format, version 0.5)
- lockfile_generated_by: `conan lock create conanfile.py -s os=Linux -s arch=x86_64 -s compiler=gcc -s compiler.version=12 -s compiler.libcxx=libstdc++11 -s build_type=Release`
- generated: 2026-04-30
- resolver_knowledge: not available (no Conan UA resolver file in knowledge cache — tree is exploratory)
- differentiator_from_test3: uses bzip2 (not poco) as runtime dep; uses conanfile.py (not conanfile.txt)
