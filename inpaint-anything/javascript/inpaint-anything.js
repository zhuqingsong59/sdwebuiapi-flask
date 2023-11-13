const inpaintAnything_waitForElement = async (parent, selector, exist) => {
    return new Promise((resolve) => {
        const observer = new MutationObserver(() => {
            if (!!parent.querySelector(selector) != exist) {
                return;
            }
            observer.disconnect();
            resolve(undefined);
        });

        observer.observe(parent, {
            childList: true,
            subtree: true,
        });

        if (!!parent.querySelector(selector) == exist) {
            resolve(undefined);
        }
    });
};

const inpaintAnything_waitForStyle = async (parent, selector, style) => {
    return new Promise((resolve) => {
        const observer = new MutationObserver(() => {
            if (!parent.querySelector(selector) || !parent.querySelector(selector).style[style]) {
                return;
            }
            observer.disconnect();
            resolve(undefined);
        });

        observer.observe(parent, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ["style"],
        });

        if (!!parent.querySelector(selector) && !!parent.querySelector(selector).style[style]) {
            resolve(undefined);
        }
    });
};

const inpaintAnything_timeout = (ms) => {
    return new Promise(function (resolve, reject) {
        setTimeout(() => reject("Timeout"), ms);
    });
};

async function inpaintAnything_clearSamMask() {
    const waitForElementToBeInDocument = (parent, selector) =>
        Promise.race([inpaintAnything_waitForElement(parent, selector, true), inpaintAnything_timeout(1000)]);

    const elemId = "#ia_sam_image";

    const targetElement = document.querySelector(elemId);
    if (!targetElement) {
        return;
    }
    await waitForElementToBeInDocument(targetElement, "button[aria-label='Clear']");

    targetElement.style.transform = null;
    targetElement.style.zIndex = null;
    targetElement.style.overflow = "auto";

    const samMaskClear = targetElement.querySelector("button[aria-label='Clear']");
    if (!samMaskClear) {
        return;
    }
    const removeImageButton = targetElement.querySelector("button[aria-label='Remove Image']");
    if (!removeImageButton) {
        return;
    }
    samMaskClear?.click();

    if (typeof inpaintAnything_clearSamMask.clickRemoveImage === "undefined") {
        inpaintAnything_clearSamMask.clickRemoveImage = () => {
            targetElement.style.transform = null;
            targetElement.style.zIndex = null;
        };
    } else {
        removeImageButton.removeEventListener("click", inpaintAnything_clearSamMask.clickRemoveImage);
    }
    removeImageButton.addEventListener("click", inpaintAnything_clearSamMask.clickRemoveImage);
}

async function inpaintAnything_clearSelMask() {
    const waitForElementToBeInDocument = (parent, selector) =>
        Promise.race([inpaintAnything_waitForElement(parent, selector, true), inpaintAnything_timeout(1000)]);

    const elemId = "#ia_sel_mask";

    const targetElement = document.querySelector(elemId);
    if (!targetElement) {
        return;
    }
    await waitForElementToBeInDocument(targetElement, "button[aria-label='Clear']");

    targetElement.style.transform = null;
    targetElement.style.zIndex = null;
    targetElement.style.overflow = "auto";

    const selMaskClear = targetElement.querySelector("button[aria-label='Clear']");
    if (!selMaskClear) {
        return;
    }
    const removeImageButton = targetElement.querySelector("button[aria-label='Remove Image']");
    if (!removeImageButton) {
        return;
    }
    selMaskClear?.click();

    if (typeof inpaintAnything_clearSelMask.clickRemoveImage === "undefined") {
        inpaintAnything_clearSelMask.clickRemoveImage = () => {
            targetElement.style.transform = null;
            targetElement.style.zIndex = null;
        };
    } else {
        removeImageButton.removeEventListener("click", inpaintAnything_clearSelMask.clickRemoveImage);
    }
    removeImageButton.addEventListener("click", inpaintAnything_clearSelMask.clickRemoveImage);
}

async function inpaintAnything_initSamSelMask() {
    inpaintAnything_clearSamMask();
    inpaintAnything_clearSelMask();
}

var uiLoadedCallbacks = [];

function gradioApp() {
    const elems = document.getElementsByTagName("gradio-app");
    const elem = elems.length == 0 ? document : elems[0];

    if (elem !== document) {
        elem.getElementById = function (id) {
            return document.getElementById(id);
        };
    }
    return elem.shadowRoot ? elem.shadowRoot : elem;
}

function onUiLoaded(callback) {
    uiLoadedCallbacks.push(callback);
}

function executeCallbacks(queue) {
    for (const callback of queue) {
        try {
            callback();
        } catch (e) {
            console.error("error running callback", callback, ":", e);
        }
    }
}

onUiLoaded(async () => {
    const elementIDs = {
        ia_sam_image: "#ia_sam_image",
        ia_sel_mask: "#ia_sel_mask",
        ia_out_image: "#ia_out_image",
        ia_cleaner_out_image: "#ia_cleaner_out_image",
    };

    function setStyleHeight(elemId, height) {
        const elem = gradioApp().querySelector(elemId);
        if (elem) {
            if (!elem.style.height) {
                elem.style.height = height;
                const observer = new MutationObserver(() => {
                    const divPreview = elem.querySelector(".preview");
                    if (divPreview) {
                        divPreview.classList.remove("fixed-height");
                    }
                });
                observer.observe(elem, {
                    childList: true,
                    attributes: true,
                    attributeFilter: ["class"],
                });
            }
        }
    }

    setStyleHeight(elementIDs.ia_out_image, "520px");
    setStyleHeight(elementIDs.ia_cleaner_out_image, "520px");

    // Default config
    const defaultHotkeysConfig = {
        canvas_hotkey_reset: "KeyR",
        canvas_hotkey_fullscreen: "KeyS",
    };

    const elemData = {};
    let activeElement;

    function applyZoomAndPan(elemId) {
        const targetElement = gradioApp().querySelector(elemId);

        if (!targetElement) {
            console.log("Element not found");
            return;
        }

        targetElement.style.transformOrigin = "0 0";

        elemData[elemId] = {
            zoomLevel: 1,
            panX: 0,
            panY: 0,
        };
        let fullScreenMode = false;

        // Toggle the zIndex of the target element between two values, allowing it to overlap or be overlapped by other elements
        function toggleOverlap(forced = "") {
            // const zIndex1 = "0";
            const zIndex1 = null;
            const zIndex2 = "998";

            targetElement.style.zIndex = targetElement.style.zIndex !== zIndex2 ? zIndex2 : zIndex1;

            if (forced === "off") {
                targetElement.style.zIndex = zIndex1;
            } else if (forced === "on") {
                targetElement.style.zIndex = zIndex2;
            }
        }

        /**
         * This function fits the target element to the screen by calculating
         * the required scale and offsets. It also updates the global variables
         * zoomLevel, panX, and panY to reflect the new state.
         */

        function fitToElement() {
            //Reset Zoom
            targetElement.style.transform = `translate(${0}px, ${0}px) scale(${1})`;

            // Get element and screen dimensions
            const elementWidth = targetElement.offsetWidth;
            const elementHeight = targetElement.offsetHeight;
            const parentElement = targetElement.parentElement;
            const screenWidth = parentElement.clientWidth;
            const screenHeight = parentElement.clientHeight;

            // Get element's coordinates relative to the parent element
            const elementRect = targetElement.getBoundingClientRect();
            const parentRect = parentElement.getBoundingClientRect();
            const elementX = elementRect.x - parentRect.x;

            // Calculate scale and offsets
            const scaleX = screenWidth / elementWidth;
            const scaleY = screenHeight / elementHeight;
            const scale = Math.min(scaleX, scaleY);

            const transformOrigin = window.getComputedStyle(targetElement).transformOrigin;
            const [originX, originY] = transformOrigin.split(" ");
            const originXValue = parseFloat(originX);
            const originYValue = parseFloat(originY);

            const offsetX = (screenWidth - elementWidth * scale) / 2 - originXValue * (1 - scale);
            const offsetY = (screenHeight - elementHeight * scale) / 2.5 - originYValue * (1 - scale);

            // Apply scale and offsets to the element
            targetElement.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${scale})`;

            // Update global variables
            elemData[elemId].zoomLevel = scale;
            elemData[elemId].panX = offsetX;
            elemData[elemId].panY = offsetY;

            fullScreenMode = false;
            toggleOverlap("off");
        }

        // Reset the zoom level and pan position of the target element to their initial values
        function resetZoom() {
            elemData[elemId] = {
                zoomLevel: 1,
                panX: 0,
                panY: 0,
            };

            // fixCanvas();
            targetElement.style.transform = `scale(${elemData[elemId].zoomLevel}) translate(${elemData[elemId].panX}px, ${elemData[elemId].panY}px)`;

            // const canvas = gradioApp().querySelector(`${elemId} canvas[key="interface"]`);

            toggleOverlap("off");
            fullScreenMode = false;

            // if (
            //     canvas &&
            //     parseFloat(canvas.style.width) > 865 &&
            //     parseFloat(targetElement.style.width) > 865
            // ) {
            //     fitToElement();
            //     return;
            // }

            // targetElement.style.width = "";
            // if (canvas) {
            //     targetElement.style.height = canvas.style.height;
            // }
            targetElement.style.width = null;
            targetElement.style.height = 480;
        }

        /**
         * This function fits the target element to the screen by calculating
         * the required scale and offsets. It also updates the global variables
         * zoomLevel, panX, and panY to reflect the new state.
         */

        // Fullscreen mode
        function fitToScreen() {
            const canvas = gradioApp().querySelector(`${elemId} canvas[key="interface"]`);
            const img = gradioApp().querySelector(`${elemId} img`);

            if (!canvas && !img) return;

            // if (canvas.offsetWidth > 862) {
            //     targetElement.style.width = canvas.offsetWidth + "px";
            // }

            if (fullScreenMode) {
                resetZoom();
                fullScreenMode = false;
                return;
            }

            //Reset Zoom
            targetElement.style.transform = `translate(${0}px, ${0}px) scale(${1})`;

            // Get scrollbar width to right-align the image
            const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;

            // Get element and screen dimensions
            const elementWidth = targetElement.offsetWidth;
            const elementHeight = targetElement.offsetHeight;
            const screenWidth = window.innerWidth - scrollbarWidth;
            const screenHeight = window.innerHeight;

            // Get element's coordinates relative to the page
            const elementRect = targetElement.getBoundingClientRect();
            const elementY = elementRect.y;
            const elementX = elementRect.x;

            // Calculate scale and offsets
            const scaleX = screenWidth / elementWidth;
            const scaleY = screenHeight / elementHeight;
            const scale = Math.min(scaleX, scaleY);

            // Get the current transformOrigin
            const computedStyle = window.getComputedStyle(targetElement);
            const transformOrigin = computedStyle.transformOrigin;
            const [originX, originY] = transformOrigin.split(" ");
            const originXValue = parseFloat(originX);
            const originYValue = parseFloat(originY);

            // Calculate offsets with respect to the transformOrigin
            const offsetX = (screenWidth - elementWidth * scale) / 2 - elementX - originXValue * (1 - scale);
            const offsetY = (screenHeight - elementHeight * scale) / 2 - elementY - originYValue * (1 - scale);

            // Apply scale and offsets to the element
            targetElement.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${scale})`;

            // Update global variables
            elemData[elemId].zoomLevel = scale;
            elemData[elemId].panX = offsetX;
            elemData[elemId].panY = offsetY;

            fullScreenMode = true;
            toggleOverlap("on");
        }

        // Reset zoom when uploading a new image
        const fileInput = gradioApp().querySelector(`${elemId} input[type="file"][accept="image/*"].svelte-116rqfv`);
        if (fileInput) {
            fileInput.addEventListener("click", resetZoom);
        }

        // Handle keydown events
        function handleKeyDown(event) {
            // Disable key locks to make pasting from the buffer work correctly
            if (
                (event.ctrlKey && event.code === "KeyV") ||
                (event.ctrlKey && event.code === "KeyC") ||
                event.code === "F5"
            ) {
                return;
            }

            // before activating shortcut, ensure user is not actively typing in an input field
            if (event.target.nodeName === "TEXTAREA" || event.target.nodeName === "INPUT") {
                return;
            }

            const hotkeyActions = {
                [defaultHotkeysConfig.canvas_hotkey_reset]: resetZoom,
                [defaultHotkeysConfig.canvas_hotkey_fullscreen]: fitToScreen,
            };

            const action = hotkeyActions[event.code];
            if (action) {
                event.preventDefault();
                action(event);
            }
        }

        // Handle events only inside the targetElement
        let isKeyDownHandlerAttached = false;

        function handleMouseMove() {
            if (!isKeyDownHandlerAttached) {
                document.addEventListener("keydown", handleKeyDown);
                isKeyDownHandlerAttached = true;

                activeElement = elemId;
            }
        }

        function handleMouseLeave() {
            if (isKeyDownHandlerAttached) {
                document.removeEventListener("keydown", handleKeyDown);
                isKeyDownHandlerAttached = false;

                activeElement = null;
            }
        }

        // Add mouse event handlers
        targetElement.addEventListener("mousemove", handleMouseMove);
        targetElement.addEventListener("mouseleave", handleMouseLeave);
    }

    applyZoomAndPan(elementIDs.ia_sam_image);
    applyZoomAndPan(elementIDs.ia_sel_mask);
    // applyZoomAndPan(elementIDs.ia_out_image);
    // applyZoomAndPan(elementIDs.ia_cleaner_out_image);
});

var executedOnLoaded = false;

document.addEventListener("DOMContentLoaded", function () {
    var mutationObserver = new MutationObserver(function () {
        if (
            !executedOnLoaded &&
            gradioApp().querySelector("#ia_sam_image") &&
            gradioApp().querySelector("#ia_sel_mask")
        ) {
            executedOnLoaded = true;
            executeCallbacks(uiLoadedCallbacks);
        }
    });
    mutationObserver.observe(gradioApp(), { childList: true, subtree: true });
});
