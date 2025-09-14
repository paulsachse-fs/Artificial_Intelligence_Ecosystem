# Use of
# Sample submission for the Building a Rule-Based AI System in Python project.
# by Paul Sachse
---
## Part 1: Initial Project Ideas

### 1. Project Idea 1: Troubleshooting Assistant
- **Description:** A system that can provide basic technology troubleshooting guidance.
- **Rule-Based Approach:**  
  - The system uses rules to guide a user through troubleshooting
  - For example, a user could say "no power" or "no internet" and recieve general guidance on next steps to take to resolve the issue.

### 2. Project Idea 2: Fortune Teller
- **Description:** A system that makes predictions about future outcomes based on input about your past.
- **Rule-Based Approach:**  
  - The system uses rules to inquire about an individual's history and provide feedback about future possiblities. 
  - For example, if someone travels often, there is a higher chance they could meet an interesting person in another location.

### 3. Project Idea 3: Emergency Assistant
- **Description:** A system that can quickly provide proper contact information or other information based on emergency context.
- **Rule-Based Approach:**  
  - The system uses rules to learn about the emergency an individual is facing and provide the most likely relevant information. 
  - For example, a fire would result immediate evacuation, where a hurriance may suggest preperation supplies, or a robbery would advise to call 911 right away.

### **Chosen Idea:** Troubleshooting Assistant
**Justification:** I chose the troubleshooting assistant, first and foremost, because I am an expert in troubleshooting technology. This means that I can ensure the system is outputting good data for the user. Furthermore, this is a practical AI application that large companies are implementing at scale today.

---

## Part 2: Rules/Logic for the Chosen System

The **Troubleshooting Assistant** system will follow these rules:

1. **Issue Identification Rule:**  
   - **IF** the user’s description contains exact keywords (e.g., “no internet”, “no power”) → **Match the problem to the correct troubleshooting category.**
   - **ELSEIF** the text contains related terms (e.g., “wifi down”, “screen black”) → **Map to the closest matching category using keyword heuristics.**
   - **ELSE** → **Notify the user that no rule exists for their issue.**

2. **Step-by-Step Assistance Rule:**  
   - **FOR EACH** step in the matched category →  
     - **Present the action to the user.**  
     - **Ask: “Did that fix it?”**
        - **IF** user responds yes → **Stop and mark issue as resolved.**
        - **IF** user responds no → **Proceed to the next step.**

3. **Resolution Rule:**  
   - **IF** any step resolves the problem → **Confirm resolution with a success message**

4. **Escalation Rule:**  
   - **IF** all troubleshooting steps fail → **Provide escalation advice**, e.g., “Seek service, contact ISP, or update drivers.”

5. **Interactive Loop Rule:**  
   - Continue asking for new problems until the user types “exit”.
   - **IF** user enters “exit” → End session with a goodbye message.

---

## Part 3: Rules/Logic for the Chosen System

Sample input and output: 

Describe the problem (e.g., 'no internet'): my computer wont turn on

=== NO POWER ===
• Try a different outlet/power strip; reseat the power cable firmly.
Did that fix it? (yes/no) n
• Desktop: ensure PSU rocker switch is ON (|). Laptop: plug in a known-good charger.
Did that fix it? (yes/no) n
• Hold power button 15–20 seconds, release, then press again.
Did that fix it? (yes/no) y
✅ Resolved!


Describe the problem (e.g., 'no internet'): my internet wont work

=== NO INTERNET ===
• Make sure Airplane Mode and any VPN are OFF, and Wi-Fi is ON.
Did that fix it? (yes/no) y
✅ Resolved!


Describe the problem (e.g., 'no internet'): my computer is slow

=== SLOW ===
• Close unused apps/tabs; save work and restart.
Did that fix it? (yes/no) n
• Ensure >10% free disk space; remove large/temp files.
Did that fix it? (yes/no) n
• Use Task Manager/Activity Monitor to end runaway processes.
Did that fix it? (yes/no) n
• Disable heavy startup apps; apply OS updates.
Did that fix it? (yes/no) n
➡️ Still not fixed. Needs deeper support/repair.

---

## Part 4: Reflection

### Project Overview:
For this project, I designed a rule-based system to assist individuals with basic technology troubleshooting. The system uses conditional decision rules to guide users step-by-step toward possible solutions. Once a user enters their issue in natural language, keywords and heuristic matches map their query to a troubleshooting category. From there, the system can walk the user through a set of diagnostic steps. After each step, the system checks with the user to see if the issue is resolved. If the issue is resolved, the system ends the interaction and returns to the beginning of the interaction loop. If the issue is not resolved, the system will proceed through additional troubleshooting steps. Eventually, if no resolution is found, the system will advise the user to reach out to the appropriate support channels. This system will continue to run in a loop, asking the user to describe a new problem, until the user types “exit”.

### Challenges:
- **Handling Many Possible Inquiries:**  
  Troubleshooting technology can come with a lot of possible user issues. This program started out with only a couple of issues it could identify, but clearly needed to have more data while it was missing troubleshooting for common issues like email and webcam issues. Once many more possible issues were added, the system became much more useful, and may actually be useful to a less technical individual. 
- **Natural Language Use:**  
  Generally, users looking for troubleshooting assistance may not have a highly technical vocabulary. That’s why an understanding of natural language had to be added to this system, which can then filter troubleshooting down to a specific workflow. Initially, a prompt like “my computer wont turn on” would return no response. Now, the semantically improved system can identify that as a “no power” issue and guide the user through appropriate steps.