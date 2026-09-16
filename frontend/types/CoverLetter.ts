import { ContactInfo } from "./Resume";

export type CoverLetter = {
  contact_info: ContactInfo;
  recipient: string;
  opening_paragraph: string;
  body_paragraphs: string[];
  closing_paragraph: string;
  signature: string;
  skills: string[];
};
