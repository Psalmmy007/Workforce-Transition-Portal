# job_risk_reference.py
#
# External, research-based automation-risk reference by job title.
#
# Source: Frey, C. B. & Osborne, M. A. (2013/2017), "The Future of Employment:
# How Susceptible Are Jobs to Computerisation?" -- the standard academic
# reference for occupational automation risk.
#
# HOW THIS WAS BUILT:
# The original study rates ~700 job titles as they existed in 2013. Several
# job titles in our dataset (Data Scientist, AI Researcher, UX Designer,
# Product Manager, Cybersecurity Analyst) did not exist as distinct
# categories back then, so there is no exact published number for them.
#
# Where a direct match exists, the tier below is based on the actual
# published figure. Where no direct match exists, the tier is a reasoned
# judgment based on the study's own explanation of *why* some jobs resist
# automation: jobs requiring negotiation, persuasion, leadership, or original
# creative/technical judgment score low; routine, single-skill analytical or
# clerical tasks score high. Each entry says which kind of judgment it is.

JOB_EXTERNAL_RISK = {
    "Marketing Specialist": {
        "tier": "High",
        "basis": "Directly sourced: 'Market Research Analysts and Marketing "
                 "Specialists' = 61% computerisation probability (Frey & Osborne)."
    },
    "Data Analyst": {
        "tier": "Medium",
        "basis": "Reasoned: analytical/reporting work has automatable "
                 "components, but interpretation and stakeholder judgment "
                 "keep it below purely clerical/routine roles."
    },
    "Cybersecurity Analyst": {
        "tier": "Medium",
        "basis": "Reasoned: routine monitoring tasks are automatable, but "
                 "responding to novel, evolving threats requires judgment "
                 "that resists automation."
    },
    "Data Scientist": {
        "tier": "Low",
        "basis": "Reasoned: original technical problem-solving is one of "
                 "the study's named automation bottlenecks."
    },
    "AI Researcher": {
        "tier": "Low",
        "basis": "Reasoned: research and original technical judgment are "
                 "named automation bottlenecks."
    },
    "Software Engineer": {
        "tier": "Low",
        "basis": "Reasoned: original software design work sits in the same "
                 "low-risk category the study assigns to applications "
                 "development roles."
    },
    "UX Designer": {
        "tier": "Low",
        "basis": "Reasoned: creativity is one of the study's named "
                 "automation bottlenecks."
    },
    "Product Manager": {
        "tier": "Low",
        "basis": "Reasoned: cross-functional leadership and negotiation "
                 "mirror 'Marketing Managers' (1.4%, directly sourced) far "
                 "more than analyst/specialist roles."
    },
    "Operations Manager": {
        "tier": "Low",
        "basis": "Reasoned: management and leadership roles are "
                 "consistently rated low-risk in the study, since they "
                 "require social/people skills."
    },
    "HR Manager": {
        "tier": "Low",
        "basis": "Reasoned: people-management roles are consistently "
                 "rated low-risk in the study."
    },
    "Sales Manager": {
        "tier": "Low",
        "basis": "Reasoned: negotiation and persuasion are explicitly "
                 "named automation bottlenecks in the study."
    },
}


def get_external_risk_tier(job_title: str) -> str:
    """Returns 'Low' / 'Medium' / 'High', or 'Unknown' if the job isn't mapped."""
    entry = JOB_EXTERNAL_RISK.get(job_title)
    return entry["tier"] if entry else "Unknown"


def get_external_risk_basis(job_title: str) -> str:
    """Returns the one-line explanation for why a job got its tier."""
    entry = JOB_EXTERNAL_RISK.get(job_title)
    return entry["basis"] if entry else "No external reference available for this title."
