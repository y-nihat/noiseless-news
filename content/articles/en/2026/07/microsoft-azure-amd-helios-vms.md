---
title: Microsoft announces three new Azure VM families built on AMD chips
date: 2026-07-20
slug: microsoft-azure-amd-helios-vms
lang: en
tldr: >
  Microsoft said on 20 July 2026 that it will build three new Azure virtual
  machine families on AMD hardware: HDv2 for data and AI workloads, HXv2 for
  chip-design and technical computing, and ND MI455X v7 for AI inference,
  the latter built on AMD's not-yet-shipping "Helios" rack-scale platform.
  AMD confirmed the same partnership in its own release. None of the VMs
  are available to customers yet — Microsoft and AMD both tie them to AMD's
  hardware shipping in the second half of 2026, a timeline some analysts
  have publicly questioned and AMD has publicly defended.
sources:
  - name: Microsoft Source (official blog)
    url: https://blogs.microsoft.com/blog/2026/07/20/microsoft-expands-azure-ai-and-hpc-infrastructure-with-amd/
  - name: AMD Newsroom
    url: https://newsroom.amd.com/news/microsoft-azure-ai-infrastructure/
  - name: Tom's Hardware
    url: https://www.tomshardware.com/tech-industry/artificial-intelligence/microsoft-will-deploy-amds-helios-rack-scale-ai-accelerator-at-scale-on-azure-radeon-instinct-mi455x-and-epyc-venice-power-will-be-available-through-redmonds-cloud-infrastructure
claims:
  - text: "On 20 July 2026 Microsoft announced three new Azure VM families running on AMD hardware: HDv2 (data-processing and AI workloads, near 500 physical 6th-gen AMD EPYC cores, 4TB RAM, 32TB local NVMe, 400Gb Azure Boost networking), HXv2 (electronic design automation and technical computing, 176 AMD 6th-gen EPYC cores at over 5GHz, up to 4TB RAM, 800Gb InfiniBand), and ND MI455X v7 (AI inference, built on AMD's Helios rack-scale platform)"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "AMD's Helios platform pairs AMD Instinct MI455X GPUs with AMD's upcoming EPYC 'Venice' CPUs; AMD's own release confirms shipments to customers, including Microsoft, beginning in the second half of 2026"
    type: announcement
    verdict: confirmed
    evidence: [2, 3]
  - text: "None of the three VM families are yet available to Azure customers — no pricing or region availability has been published; Microsoft and AMD both frame this as tied to AMD hardware shipping in H2 2026"
    type: announcement
    verdict: confirmed
    evidence: [1, 2, 3]
  - text: "The announcement builds on an existing Microsoft-AMD collaboration: Azure's HX-series VMs, using AMD 3D V-Cache technology, first launched in partnership with AMD in 2023"
    type: announcement
    verdict: confirmed
    evidence: [1]
updated: []
---

## What happened

Microsoft said on 20 July 2026 that it is expanding Azure's AI and
high-performance-computing infrastructure with three new virtual machine
families built on AMD hardware [1]. HDv2 targets data processing and AI
workloads, with close to 500 physical 6th-generation AMD EPYC cores, 4
terabytes of RAM, 32 terabytes of local NVMe storage, and 400Gb Azure Boost
networking per instance [1]. HXv2 targets electronic design automation and
other technical computing, with 176 AMD 6th-generation EPYC cores clocked
above 5GHz, up to 4 terabytes of RAM, and 800Gb InfiniBand networking [1].
ND MI455X v7 is built for AI inference on AMD's "Helios" rack-scale
platform, which combines AMD Instinct MI455X GPUs with AMD's upcoming EPYC
"Venice" CPUs [1].

AMD published a matching release the same day confirming the partnership
and stating that Helios-based shipments to customers, including Microsoft,
begin in the second half of 2026 [2]. Independent outlets including Tom's
Hardware, CNBC, SiliconANGLE and StorageReview covered the announcement
same-day with matching specifications [3]. Neither company has published
pricing or a region-availability date for any of the three VM families;
both tie general availability to AMD's H2 2026 hardware shipment timeline
[1][2]. Microsoft frames the news as an extension of Azure's existing
AMD collaboration, noting its HX-series VMs first launched with AMD in
2023 using AMD's 3D V-Cache technology [1].

That H2 2026 shipment timeline has drawn public disagreement: a February
2026 report questioned whether MI455X volume production would slip to
2027, which AMD's software leadership publicly disputed at the time,
saying Helios remained on track for the second half of 2026 [3].

## Why it matters

This is a concrete expansion of Microsoft's multi-vendor chip strategy for
Azure, adding AMD-based inference and technical-computing capacity
alongside its existing Nvidia-based offerings — relevant to how much
AI compute capacity becomes available and from how many suppliers.
Because none of the three VM families can be provisioned yet, the
practical effect depends on whether AMD's second-half-2026 shipment
timeline holds.
