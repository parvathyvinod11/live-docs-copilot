import pathway as pw

docs = pw.io.fs.read(
    "./data/docs",
    format="plaintext",
    with_metadata=True,
    autocommit_duration_ms=1000
)

def analyze_change(path, content):
    if path.endswith(".swp"):
        return

    verdict = "ℹ️ Non-breaking update"

    breaking_keywords = [
        "removed",
        "deprecated",
        "mandatory",
        "breaking",
        "no longer supported"
    ]

    for word in breaking_keywords:
        if word.lower() in content.lower():
            verdict = "⚠️ BREAKING CHANGE DETECTED"
            break

    print("\n📄 DOCUMENT UPDATE DETECTED")
    print("Path:", path)
    print("Verdict:", verdict)
    print("Content:")
    print(content)
    print("-" * 60)

docs = docs.select(
    path=docs.metadata["path"],
    content=docs.data,
    _=pw.apply(analyze_change, docs.metadata["path"], docs.data)
)

pw.debug.compute_and_print(docs)
