// MINISTRY OF SECRET NUMBERS - TERMINAL SCRIPT B-9

document.addEventListener('DOMContentLoaded', () => {
    const generateForm = document.getElementById('generate-form');
    const validateForm = document.getElementById('validate-form');
    const outputScreen = document.getElementById('output-screen');
    const prompt = document.getElementById('prompt');
    const methodSelect = document.getElementById('method');
    const uniqueOptions = document.getElementById('unique-options');

    const typeText = (element, text) => {
        return new Promise((resolve) => {
            element.innerHTML = '';
            let i = 0;
            function typing() {
                if (i < text.length) {
                    let char = text.charAt(i);
                    if (char === '\n') {
                        element.innerHTML += '<br>';
                    } else {
                        element.innerHTML += char;
                    }
                    i++;
                    outputScreen.scrollTop = outputScreen.scrollHeight;
                    setTimeout(typing, 10);
                } else {
                    resolve();
                }
            }
            typing();
        });
    };

    const clearOutput = () => {
        outputScreen.innerHTML = '';
    };
    
    const showPrompt = () => {
        outputScreen.appendChild(prompt);
        prompt.style.display = 'inline-block';
        outputScreen.scrollTop = outputScreen.scrollHeight;
    };

    const hidePrompt = () => {
        prompt.style.display = 'none';
    };

    const displayOutput = async (lines) => {
        hidePrompt();
        clearOutput();
        for (const line of lines) {
            const p = document.createElement('p');
            if (line.type === 'error') {
                p.className = 'error';
            } else if (line.type === 'success') {
                p.className = 'success';
            }
            outputScreen.appendChild(p);
            await typeText(p, line.text);
        }
        showPrompt();
    };

    methodSelect.addEventListener('change', () => {
        uniqueOptions.disabled = methodSelect.value !== 'unique';
    });
    // Trigger change on load
    methodSelect.dispatchEvent(new Event('change'));


    generateForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(generateForm);
        const params = new URLSearchParams();

        params.append('num', formData.get('num'));
        params.append('method', formData.get('method'));

        if (formData.get('method') === 'unique') {
            params.append('sex', formData.get('sex'));
            params.append('start_date', formData.get('start_date'));
            params.append('end_date', formData.get('end_date'));
        }
        
        await displayOutput([
            { text: `> INITIATING REQUISITION C-7...`},
            { text: `> QUERYING DATABASE WITH PROTOCOL: ${formData.get('method').toUpperCase()}...`}
        ]);

        try {
            const response = await fetch(`/generate/?${params.toString()}`, {
                method: 'POST',
                headers: { 'accept': 'application/json' }
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail);
            }

            const outputLines = [
                { text: `> OPERATION SUCCESSFUL. MANIFEST GENERATED:`, type: 'success' },
                { text: `------------------------------------------` },
                ...data.pesels.map(p => ({ text: p })),
                { text: `------------------------------------------` },
                { text: `> TOTAL IDENTITIES FABRICATED: ${data.pesels.length}` },
            ];
            await displayOutput(outputLines);

        } catch (error) {
            await displayOutput([
                { text: `> SYSTEM ERROR: ${error.message}`, type: 'error' },
                { text: `> ABORTING OPERATION.`}
            ]);
        }
    });

    validateForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(validateForm);
        const pesel = formData.get('pesel');
        
        await displayOutput([
            { text: `> VALIDATING CREDENTIAL: ${pesel}...`}
        ]);

        try {
            const response = await fetch(`/validate/?pesel=${encodeURIComponent(pesel)}`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail);
            }
            
            const resultText = data.is_valid ? 'AUTHENTIC' : 'INVALID OR FORGED';
            const resultType = data.is_valid ? 'success' : 'error';

            await displayOutput([
                { text: `> VALIDATION COMPLETE.`},
                { text: `> STATUS: ${resultText}`, type: resultType }
            ]);

        } catch (error) {
            await displayOutput([
                { text: `> VALIDATION FAILED: ${error.message}`, type: 'error' }
            ]);
        }
    });
}); 