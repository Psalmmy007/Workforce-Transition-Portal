# skill_engine.py
# Algorithmic Skill Adjacency Engine with Risk-Aware Career Navigation

# 1. Canonical Expert-Curated Role Competency Profiles
# Note: Manually authored domain baselines reflecting industry task standards
ROLE_SKILL_PROFILES = {
    "Data Analyst": ["SQL", "Excel", "Data Analysis", "Tableau", "Communication"],
    "Data Scientist": ["Python", "Machine Learning", "Data Analysis", "Statistics", "SQL"],
    "AI Researcher": ["Python", "Machine Learning", "Deep Learning", "Data Analysis", "Research"],
    "Cybersecurity Analyst": ["Cybersecurity", "Python", "Data Analysis", "Project Management", "Communication"],
    "Software Engineer": ["Python", "JavaScript", "SQL", "Project Management", "Communication"],
    "UX Designer": ["UX/UI Design", "Communication", "Project Management", "JavaScript", "Data Analysis"],
    "Product Manager": ["Project Management", "Communication", "Data Analysis", "Marketing", "Sales"],
    "Operations Manager": ["Project Management", "Communication", "Data Analysis", "Operations", "Leadership"],
    "Marketing Specialist": ["Marketing", "Communication", "Data Analysis", "Project Management", "Sales"],
    "HR Manager": ["Communication", "Project Management", "Leadership", "Talent Acquisition", "Data Analysis"],
    "Sales Manager": ["Sales", "Communication", "Negotiation", "Leadership", "Project Management"]
}

# 2. Risk-Aware Transition Pathways
# High risk steers toward roles resilient to automation; Low risk prioritizes vertical leadership
RESILIENT_PIVOTS = {
    "Data Analyst": ["Data Scientist", "Product Manager", "Cybersecurity Analyst"],
    "Marketing Specialist": ["Product Manager", "Data Analyst", "Sales Manager"],
    "UX Designer": ["Product Manager", "Software Engineer"],
    "HR Manager": ["Operations Manager", "Product Manager"],
    "Sales Manager": ["Product Manager", "Operations Manager"],
    "Software Engineer": ["AI Researcher", "Cybersecurity Analyst"],
    "Operations Manager": ["Product Manager", "Data Analyst"],
    "AI Researcher": ["Data Scientist", "Software Engineer"],
    "Cybersecurity Analyst": ["Software Engineer", "Operations Manager"],
    "Data Scientist": ["AI Researcher", "Product Manager"],
    "Product Manager": ["Operations Manager", "Sales Manager"]
}

GROWTH_PIVOTS = {
    "Data Analyst": ["Data Scientist", "AI Researcher"],
    "Data Scientist": ["AI Researcher", "Product Manager"],
    "Software Engineer": ["AI Researcher", "Cybersecurity Analyst"],
    "Marketing Specialist": ["Product Manager", "Operations Manager"],
    "UX Designer": ["Product Manager"],
    "HR Manager": ["Operations Manager"],
    "Sales Manager": ["Operations Manager"],
    "Operations Manager": ["Product Manager"],
    "Cybersecurity Analyst": ["AI Researcher", "Software Engineer"],
    "AI Researcher": ["Data Scientist"],
    "Product Manager": ["Operations Manager"]
}

def clean_skill_label(skill_name: str) -> str:
    """Safely normalizes skill names without corrupting slashes or standard acronyms."""
    s = skill_name.strip()
    special_cases = {
        "ux/ui design": "UX/UI Design",
        "sql": "SQL",
        "crm": "CRM",
        "seo": "SEO",
        "hr systems": "HR Systems",
        "ai researcher": "AI Researcher"
    }
    if s.lower() in special_cases:
        return special_cases[s.lower()]
    # Preserve proper casing around slashes
    if "/" in s:
        return "/".join(part.strip().capitalize() for part in s.split("/"))
    return s.title()

def calculate_similarity(user_skills, target_skills):
    """Computes exact set overlap percentage between user competencies and target prerequisites."""
    user_set = set([clean_skill_label(s) for s in user_skills])
    target_set = set([clean_skill_label(s) for s in target_skills])
    
    if not target_set:
        return 0.0
    
    overlap = user_set.intersection(target_set)
    return round((len(overlap) / len(target_set)) * 100, 1)

def get_career_recommendations(current_role, user_skills, predicted_risk="High"):
    """
    Risk-Aware Recommender:
    - If High/Medium risk: Prioritizes automation-resilient pivots and immediate lateral safety.
    - If Low risk: Prioritizes advanced vertical growth and strategic specialization.
    """
    user_set = set([clean_skill_label(s) for s in user_skills])
    recommendations = []
    
    # Connect risk prediction directly to pivot selection logic
    if predicted_risk in ["High", "Medium"]:
        candidate_roles = RESILIENT_PIVOTS.get(current_role, list(ROLE_SKILL_PROFILES.keys()))
        strategy_context = "Defensive Pivot (Resilient Role)"
    else:
        candidate_roles = GROWTH_PIVOTS.get(current_role, list(ROLE_SKILL_PROFILES.keys()))
        strategy_context = "Vertical Specialization"

    for role in candidate_roles:
        if role == current_role:
            continue
        
        target_skills = ROLE_SKILL_PROFILES.get(role, [])
        target_set = set([clean_skill_label(s) for s in target_skills])
        
        matching_skills = sorted(list(user_set.intersection(target_set)))
        missing_skills = sorted(list(target_set - user_set))
        match_score = calculate_similarity(user_skills, target_skills)
        
        recommendations.append({
            "target_role": role,
            "match_score": match_score,
            "matching_skills": matching_skills,
            "skills_to_learn": missing_skills,
            "strategy": strategy_context
        })
    
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations