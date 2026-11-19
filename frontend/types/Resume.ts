export type ContactInfo = {
  name: string;
  email: string;
  phone: string;
  location: string;
  links: string[];
};

export type Education = {
  degree: string;
  institution: string;
  start_date: string;
  end_date: string;
  relevant_courses: string[];
};

export type Experience = {
  title: string;
  company: string;
  start_date: string;
  end_date: string;
  responsibilities: string[];
};

export type Project = {
  name: string;
  technologies: string[];
  start_date: string;
  end_date: string;
  description: string[];
};

export type SkillGroup = {
  category: string;
  skills: string[];
};

export type Resume = {
  contact_info: ContactInfo;
  skills: string[];
  skill_groups?: SkillGroup[];
  education: Education[];
  experience: Experience[];
  projects: Project[];
};
