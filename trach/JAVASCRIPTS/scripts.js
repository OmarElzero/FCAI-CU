    const typed = new Typed('.hello', {
        strings: ["Hello, I'm Omar Betawy!" , "Software Engnieer","Problem Slover" , "Ai Trainer" ],
        typeSpeed: 100,
        backSpeed:100,
        backDelay:600,
        loop :true
    
    });

    const typ = new Typed('.abo', {
        strings: ["Hello, I'm Omar Betawy!","I am a dedicated Software Engineer with a strong background in foundational concepts of C, Python, DevOps, and Linux, honed during a comprehensive 14-month internship with ALX Africa.My experience includes working on diverse projects such as an Airbnb project, where I gained practical skills in patching, scripting, and managing web servers."
    ,"As a Problem Solver, I thrive on tackling complex challenges and finding innovative solutions. My passion for technology and continuous learning has driven me to explore various aspects of software development and AI."
    ,"In addition to my technical expertise, I am also an AI Trainer. I have taken several courses with Google, including 'Introduction to Responsible AI,' 'Introduction to Generative AI,' and 'Introduction to Large Language Models.' This knowledge allows me to stay at the forefront of AI advancements and share insights with others."
    ,"Whether I'm coding, training AI models, or optimizing online marketing campaigns with GrowPro, my commitment to excellence and innovation remains unwavering. Let's connect and explore the possibilities together!"],
        typeSpeed: 150,
        backSpeed:100,
        backDelay:600,
        loop :true
    
    });

    const t = new Typed('.j1', {
        strings: ["During my 14-month internship with ALX Africa, I worked on foundational concepts in C and Python, DevOps, Linux, patching, scripting, and web servers. One of the key projects I contributed to was an Airbnb project." ],
        typeSpeed: 150,
        backSpeed:100,
        backDelay:600,
        loop :true
    
    });
    const t1 = new Typed('.j2', {
        strings: ["At Founder Academy, I developed leadership skills and gained valuable insights into startup culture and business management, enhancing my entrepreneurial mindset." ],
        typeSpeed: 150,
        backSpeed:100,
        backDelay:600,
        loop :true
    
    });
    const t2 = new Typed('.j3', {
        strings: ["As an AI Trainer, I completed several courses with Google, including \'Introduction to Responsible AI,\', \'Introduction to Generative AI,\', and \'Introduction to Large Language Models.\' I shared my knowledge and insights with others, helping them understand and apply AI concepts effectively. At Outlier AI, I work on developing large language models (LLMs)." ],
        typeSpeed: 150,
        backSpeed:100,
        backDelay:600,
        loop :true
    
    });


    function showExperienceDetails(id) {
        const details = document.getElementById(id);
        if (details.style.display === "none" || details.style.display === "") {
            details.style.display = "block";
        } else {
            details.style.display = "none";
        }
    }


    
