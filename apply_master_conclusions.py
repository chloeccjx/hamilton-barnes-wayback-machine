import json
from copy import deepcopy
from pathlib import Path

JSON_PATH = Path("data/content.json")

MASTER_CONCLUSIONS = {
    "Network Automation": [
        "Across the decade, network automation has shifted from being an efficiency tool to becoming foundational infrastructure. What began as scripting and task acceleration has evolved into platform engineering, lifecycle management and compliance control at scale.",
        "The trajectory reflects complexity. Networks are larger, more distributed and more business critical than ever before. Human operated configuration alone is no longer sustainable in high velocity environments.",
        "Going forward, automation capability will define operational maturity. Organisations will prioritise engineers who can design, validate and evolve automated systems rather than simply operate individual devices."
    ],
    "Enterprise Networking": [
        "Enterprise networking has transitioned from static infrastructure to dynamic service architecture. Connectivity is no longer just about uptime but about experience, visibility and adaptability.",
        "As traffic patterns, applications and workforces decentralise, network design must anticipate change rather than react to it.",
        "The long term direction is clear. Enterprise networking roles increasingly require architectural thinking, policy driven control and cross domain awareness across cloud, edge and security environments."
    ],
    "Cloud & Infrastructure": [
        "Cloud and infrastructure have converged into unified platform thinking. The separation between on premises and cloud environments has steadily diminished as hybrid models became operational reality.",
        "Infrastructure is now measured by flexibility, resilience and scalability rather than hardware ownership.",
        "Over the next phase, engineers who understand distributed system behaviour, workload orchestration and platform design will define the next generation of infrastructure leadership."
    ],
    "Cybersecurity": [
        "Cybersecurity has evolved from perimeter defence into continuous risk management. The attack surface has expanded while regulatory expectations have intensified.",
        "Security is no longer a standalone function but an embedded discipline across infrastructure, identity, development and governance.",
        "The defining capability moving forward will be adaptability. Organisations will prioritise professionals who combine technical depth with strategic risk communication and cross functional awareness."
    ],
    "IP Networking": [
        "IP networking has become the universal transport layer underpinning nearly all modern connectivity. What was once a specialised domain is now foundational to cloud, mobile and enterprise ecosystems.",
        "Scalability, latency and resilience requirements have accelerated alongside data growth.",
        "Future IP environments will demand engineers capable of integrating physical infrastructure, software driven control and performance optimisation across distributed architectures."
    ],
    "Radio Frequency": [
        "Radio frequency engineering has progressed from coverage optimisation to real time performance orchestration. Spectrum efficiency and density management now operate at unprecedented scale.",
        "The complexity of modern deployments requires data driven modelling and adaptive optimisation.",
        "RF roles increasingly blend traditional engineering knowledge with analytics, automation and system level coordination."
    ],
    "Satellite": [
        "Satellite connectivity has transitioned from niche fallback solution to integrated component of global connectivity strategies.",
        "Reduced latency and expanded constellations have repositioned satellite within enterprise and resilience planning.",
        "The next phase will centre on hybrid integration, where satellite and terrestrial networks operate as coordinated layers within unified architectures."
    ],
    "Broadcasting": [
        "Broadcasting has shifted from hardware centric transmission to IP based content ecosystems. Infrastructure flexibility now defines competitiveness.",
        "Cloud integration and multi platform distribution have reshaped workflows.",
        "Future broadcasting expertise will depend on interoperability, software proficiency and the ability to operate within converged media and networking environments."
    ],
    "Fibre Networking": [
        "Fibre has moved from expansion phase to strategic backbone status. It underpins cloud growth, mobile evolution and enterprise transformation.",
        "Deployment maturity now focuses on scalability, resilience and long term demand forecasting rather than short term capacity fixes.",
        "Fibre engineering will remain central to digital infrastructure, requiring coordinated planning across technology, regulation and capital investment."
    ],
    "Civil Engineering": [
        "Civil engineering has become a primary enabler of digital infrastructure rather than a supporting afterthought.",
        "Large scale rollout programs require coordination, geospatial precision and regulatory alignment.",
        "As connectivity becomes essential infrastructure, civil roles will continue to expand in strategic importance across planning, sustainability and resilience."
    ],
    "AI Data Centers": [
        "AI data centres represent a structural transformation in compute design. Power density, cooling and interconnect performance now shape strategic location decisions.",
        "Infrastructure has shifted from general enterprise hosting to specialised high intensity compute environments.",
        "Sustained growth will depend on energy innovation, supply chain coordination and long term capital planning."
    ],
    "AI Software & Networks": [
        "AI software and networking have become interdependent domains. Model performance is increasingly constrained by network architecture rather than compute alone.",
        "Distributed training, inference and orchestration require tightly engineered data flows.",
        "Future AI ecosystems will prioritise low latency fabrics, topology optimisation and software defined network intelligence."
    ],
    "Data Centre IT": [
        "Data centre IT has evolved from server maintenance to platform operations. Workloads are dynamic, automated and increasingly AI driven.",
        "Operational excellence now requires observability, orchestration and cross environment integration.",
        "The next phase will emphasise workload optimisation, automation literacy and resilience across hybrid infrastructures."
    ],
    "Critical Facilities & Data Centre Construction": [
        "Critical facilities have emerged as a limiting factor in digital expansion. Power availability and cooling innovation now shape infrastructure viability.",
        "Construction strategy increasingly intersects with sustainability, grid integration and long term energy planning.",
        "The future of data centre construction will centre on enabling compute capacity at scale while balancing environmental and regulatory constraints."
    ],
}

def main():
    if not JSON_PATH.exists():
        raise SystemExit(f"Missing: {JSON_PATH.resolve()}")

    content = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    updated_specialisms = 0
    updated_years = 0
    missing = []

    for specialism, payload in content.items():
        master = MASTER_CONCLUSIONS.get(specialism)
        if not master:
            missing.append(specialism)
            continue

        years = (payload or {}).get("years") or {}
        if not isinstance(years, dict) or not years:
            continue

        for year_key, year_payload in years.items():
            if not isinstance(year_payload, dict):
                years[year_key] = {}
                year_payload = years[year_key]

            year_payload["conclusion"] = deepcopy(master)
            updated_years += 1

        updated_specialisms += 1

    JSON_PATH.write_text(json.dumps(content, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Updated conclusions for {updated_specialisms} specialisms across {updated_years} years.")
    if missing:
        print("⚠️ No master conclusion found for these specialisms (names must match exactly):")
        for m in missing:
            print(f" - {m}")

if __name__ == "__main__":
    main()