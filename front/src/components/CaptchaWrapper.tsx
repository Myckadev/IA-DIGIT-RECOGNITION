import React, { useState } from "react";
import ReCAPTCHA from "react-google-recaptcha";
import Canva from "./Canva";

const SITE_KEY = "6LceadYqAAAAACDf8KZRYgOL_1BI-YBpFceWZbv0";

export default function CaptchaWrapper() {
    const [captchaVerified, setCaptchaVerified] = useState<boolean>(false);

    const handleCaptcha = (token: string | null) => {
        if (token) {
            setCaptchaVerified(true);
        } else {
            setCaptchaVerified(false);
        }
    };

    return (
        <div>
            {captchaVerified ? (
                <Canva />
            ) : (
                <div style={{ textAlign: "center", marginTop: "50px" }}>
                    <h2>Veuillez compléter le reCAPTCHA pour accéder au centre de tri</h2>
                    <ReCAPTCHA
                        sitekey={SITE_KEY}
                        onChange={handleCaptcha}
                        style={{
                            display: "flex",
                            justifyContent: "center"
                        }}
                    />
                </div>
            )}
        </div>
    );
}
