// ============================================
// INTELLIGENT EMAIL ASSISTANT
// Frontend JavaScript
// ============================================


// Get HTML elements

const emailForm = document.getElementById("emailForm");

const generateButton = document.getElementById("generateButton");

const loading = document.getElementById("loading");

const message = document.getElementById("message");

const toneSelect = document.getElementById("tone");

const improveToneButton = document.getElementById("improveToneButton");

const saveButton = document.getElementById("saveButton");


// Store the latest analysis result

let analysisData = null;


// ============================================
// HELPER FUNCTIONS
// ============================================


// Display success or error messages

function showMessage(text, isError = false) {

    message.textContent = text;

    message.classList.remove("hidden", "error");

    if (isError) {
        message.classList.add("error");
    }

}


// Clear messages

function clearMessage() {

    message.classList.add("hidden");

    message.classList.remove("error");

}


// Safely update text elements

function setText(id, value) {

    const element = document.getElementById(id);

    if (element) {
        element.textContent = value || "Not available.";
    }

}


// Get the customer details directly from the form

function getCustomerDetails() {

    return {

        customer_name: document
            .getElementById("customerName")
            .value
            .trim(),

        subject: document
            .getElementById("subject")
            .value
            .trim(),

        customer_email: document
            .getElementById("customerEmail")
            .value
            .trim()

    };

}


// Get the currently displayed reply

function getCurrentReply() {

    const toneReply = document
        .getElementById("toneReply")
        .value
        .trim();

    const generatedReply = document
        .getElementById("generatedReply")
        .value
        .trim();

    // Prefer the tone-improved reply if available

    if (toneReply) {
        return toneReply;
    }

    return generatedReply;

}


// Send a JSON request to Flask

async function postJSON(url, data) {

    const response = await fetch(url, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    });

    const result = await response.json();

    if (!response.ok || !result.success) {

        throw new Error(
            result.error || "Something went wrong."
        );

    }

    return result;

}


// ============================================
// 1. GENERATE AI RESPONSE
// ============================================


emailForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    clearMessage();

    const customer = getCustomerDetails();

    const selectedTone = toneSelect.value;


    // Validate input

    if (
        !customer.customer_name ||
        !customer.subject ||
        !customer.customer_email
    ) {

        showMessage(
            "Please fill in all the customer email fields.",
            true
        );

        return;

    }


    // Reset old results before starting a new analysis

    analysisData = null;

    document.getElementById("intentBadge").textContent =
        "Analyzing...";

    document.getElementById("previousEmail").textContent =
        "Searching historical emails...";

    document.getElementById("previousReply").textContent =
        "Retrieving previous reply...";

    document.getElementById("summary").textContent =
        "Generating summary...";

    document.getElementById("generatedReply").value = "";

    document.getElementById("toneReply").value = "";


    generateButton.disabled = true;

    loading.classList.remove("hidden");

    generateButton.textContent = "Generating Response...";


    try {

        // Send customer email to Flask

        const result = await postJSON(
            "/analyze",
            {
                ...customer,
                tone: selectedTone
            }
        );


        // Store analysis data

        analysisData = result;


        // Display detected intent

        setText(
            "intentBadge",
            result.intent
        );


        // Display similar historical email

        setText(
            "previousEmail",
            result.previous_email
        );


        // Display previous reply

        setText(
            "previousReply",
            result.previous_reply
        );


        // Display conversation summary

        setText(
            "summary",
            result.summary
        );


        // Display generated reply

        document.getElementById("generatedReply").value =
            result.generated_reply || "";


        // Display tone-improved reply

        document.getElementById("toneReply").value =
            result.tone_reply || "";


        // Update selected tone

        toneSelect.value = result.tone || selectedTone;

        document.getElementById("toneBadge").textContent =
            toneSelect.value;


        showMessage(
            "Email analyzed successfully!"
        );


    } catch (error) {

        console.error(
            "Analysis error:",
            error
        );

        showMessage(
            "Unable to analyze email: " + error.message,
            true
        );

    } finally {

        loading.classList.add("hidden");

        generateButton.disabled = false;

        generateButton.innerHTML =
            "<span>✦</span> Generate AI Response";

    }

});


// ============================================
// 2. UPDATE TONE LABEL
// ============================================


toneSelect.addEventListener("change", function () {

    document.getElementById("toneBadge").textContent =
        toneSelect.value;

});


// ============================================
// 3. IMPROVE TONE
// ============================================


improveToneButton.addEventListener("click", async function () {

    clearMessage();


    // Get the reply directly from the visible textarea

    const generatedReply = document
        .getElementById("generatedReply")
        .value
        .trim();


    if (!generatedReply) {

        showMessage(
            "Please generate an AI reply before improving its tone.",
            true
        );

        return;

    }


    const selectedTone = toneSelect.value;


    improveToneButton.disabled = true;

    improveToneButton.textContent = "Improving Tone...";


    try {

        // Call Flask tone-improvement endpoint

        const result = await postJSON(
            "/improve-tone",
            {
                reply: generatedReply,
                tone: selectedTone
            }
        );


        // Display improved reply

        document.getElementById("toneReply").value =
            result.reply;


        // Update tone label

        document.getElementById("toneBadge").textContent =
            result.tone;


        showMessage(
            "Reply successfully rewritten in " +
            result.tone +
            " tone!"
        );


    } catch (error) {

        console.error(
            "Tone improvement error:",
            error
        );

        showMessage(
            "Unable to improve tone: " + error.message,
            true
        );

    } finally {

        improveToneButton.disabled = false;

        improveToneButton.textContent =
            "Improve Tone";

    }

});


// ============================================
// 4. SAVE REPLY
// ============================================


saveButton.addEventListener("click", async function () {

    clearMessage();


    // Get current values directly from the form

    const customer = getCustomerDetails();


    // Get the detected intent displayed on the page

    const intent = document
        .getElementById("intentBadge")
        .textContent
        .trim();


    // Get the currently displayed reply

    const generatedReply = getCurrentReply();


    // Validate required information

    if (
        !customer.customer_name ||
        !customer.subject ||
        !customer.customer_email
    ) {

        showMessage(
            "Please enter the customer name, subject, and email.",
            true
        );

        return;

    }


    if (
        !intent ||
        intent === "Analyzing..." ||
        intent === "Awaiting Analysis"
    ) {

        showMessage(
            "Please click Generate AI Response before saving.",
            true
        );

        return;

    }


    if (!generatedReply) {

        showMessage(
            "There is no reply to save. Generate a reply first.",
            true
        );

        return;

    }


    // Disable button during saving

    saveButton.disabled = true;

    saveButton.textContent = "Saving...";


    try {

        // Send all required data to Flask

        const result = await postJSON(
            "/save",
            {
                customer_name: customer.customer_name,
                subject: customer.subject,
                customer_email: customer.customer_email,
                intent: intent,
                generated_reply: generatedReply
            }
        );


        showMessage(
            result.message +
            " Saved to: " +
            result.file
        );


    } catch (error) {

        console.error(
            "Save error:",
            error
        );

        showMessage(
            "Unable to save reply: " + error.message,
            true
        );

    } finally {

        saveButton.disabled = false;

        saveButton.textContent = "Save Reply";

    }

});


// ============================================
// 5. COPY GENERATED REPLY
// ============================================


document
    .querySelectorAll("[data-copy]")
    .forEach(function (button) {

        button.addEventListener("click", async function () {

            const targetId = button.dataset.copy;

            const text = document
                .getElementById(targetId)
                .value
                .trim();


            if (!text) {

                showMessage(
                    "There is no reply to copy.",
                    true
                );

                return;

            }


            try {

                await navigator.clipboard.writeText(text);

                showMessage(
                    "Reply copied successfully!"
                );

            } catch (error) {

                showMessage(
                    "Unable to copy automatically. Please select and copy the text manually.",
                    true
                );

            }

        });

    });