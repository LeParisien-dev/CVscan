// Declare minimal interfaces for the Web Speech API
interface SpeechRecognition extends EventTarget {
    lang: string;
    continuous: boolean;
    interimResults: boolean;
    start(): void;
    stop(): void;
    abort(): void;
    onaudioend?: (this: SpeechRecognition, ev: Event) => any;
    onaudiostart?: (this: SpeechRecognition, ev: Event) => any;
    onend?: (this: SpeechRecognition, ev: Event) => any;
    onerror?: (this: SpeechRecognition, ev: Event) => any;
    onnomatch?: (this: SpeechRecognition, ev: Event) => any;
    onresult?: (this: SpeechRecognition, ev: SpeechRecognitionEvent) => any;
    onsoundend?: (this: SpeechRecognition, ev: Event) => any;
    onsoundstart?: (this: SpeechRecognition, ev: Event) => any;
    onspeechend?: (this: SpeechRecognition, ev: Event) => any;
    onspeechstart?: (this: SpeechRecognition, ev: Event) => any;
    onstart?: (this: SpeechRecognition, ev: Event) => any;
}

interface SpeechRecognitionEvent extends Event {
    readonly resultIndex: number;
    readonly results: SpeechRecognitionResultList;
}

declare var SpeechRecognition: {
    prototype: SpeechRecognition;
    new(): SpeechRecognition;
};

declare var webkitSpeechRecognition: {
    prototype: SpeechRecognition;
    new(): SpeechRecognition;
};
