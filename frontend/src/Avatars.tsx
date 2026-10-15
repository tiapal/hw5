import type { AgentKey } from "./agents";

// Hand-drawn SVG people (no photos, no image services). Each is 120 x 150: head and shoulders.
const SKIN = "#efc8a2";
const INK = "#2b2118";

type Props = { working?: boolean };

// The Boss: old grandfather, bald on top, white tufts, bushy brows, oak jacket (same oak as the table).
function Boss() {
  return (
    <svg viewBox="0 0 120 150" role="img" aria-label="The Boss, an old patriarch in an oak jacket">
      <path d="M6 150 Q8 106 60 102 Q112 106 114 150 Z" fill="#9a6a2b" />
      <path d="M60 102 L44 150 L60 128 L76 150 Z" fill="#f4ece0" />
      <path d="M60 110 L54 150 L66 150 Z" fill="#3b2a1e" />
      <path d="M44 106 L36 150 L46 150 L58 112 Z M76 106 L84 150 L74 150 L62 112 Z" fill="#7b5220" />
      <circle cx="84" cy="124" r="3.5" fill="#e3c25a" />
      <ellipse cx="60" cy="62" rx="31" ry="37" fill={SKIN} />
      <circle cx="29" cy="64" r="10" fill="#f6f6f2" />
      <circle cx="91" cy="64" r="10" fill="#f6f6f2" />
      <circle cx="31" cy="52" r="7" fill="#f6f6f2" />
      <circle cx="89" cy="52" r="7" fill="#f6f6f2" />
      <ellipse cx="50" cy="34" rx="12" ry="5" fill="#fff" opacity=".35" />
      <path d="M40 54 Q50 44 58 53" stroke="#f6f6f2" strokeWidth="6" fill="none" strokeLinecap="round" />
      <path d="M62 53 Q70 44 80 54" stroke="#f6f6f2" strokeWidth="6" fill="none" strokeLinecap="round" />
      <path d="M44 62 q6 -3 12 0 M64 62 q6 -3 12 0" stroke={INK} strokeWidth="2.4" fill="none" strokeLinecap="round" />
      <circle cx="50" cy="65" r="2" fill={INK} />
      <circle cx="70" cy="65" r="2" fill={INK} />
      <path d="M42 46 q18 -6 36 0" stroke="#c8a583" strokeWidth="1.3" fill="none" />
      <path d="M45 41 q15 -5 30 0" stroke="#c8a583" strokeWidth="1.3" fill="none" />
      <path d="M60 66 q-7 12 -2 15 q4 2 8 0" stroke="#c99974" strokeWidth="2.4" fill="none" strokeLinecap="round" />
      <path d="M48 88 q12 -5 24 0" stroke="#7a4b3a" strokeWidth="3" fill="none" strokeLinecap="round" />
      <path d="M46 78 q4 4 4 9 M74 78 q-4 4 -4 9" stroke="#c99974" strokeWidth="1.3" fill="none" />
    </svg>
  );
}

// Ina: about fifty, round glasses, hair in a bun with a grey streak, navy cardigan.
function Ina() {
  return (
    <svg viewBox="0 0 120 150" role="img" aria-label="Inventory Ina, a woman in her fifties with glasses and a navy cardigan">
      <path d="M8 150 Q10 108 60 104 Q110 108 112 150 Z" fill="#1f3a6e" />
      <path d="M60 104 L50 150 M60 104 L70 150" stroke="#162a52" strokeWidth="2" />
      <circle cx="56" cy="128" r="2.5" fill="#d9c27a" />
      <circle cx="56" cy="140" r="2.5" fill="#d9c27a" />
      <circle cx="60" cy="22" r="14" fill="#4a3427" />
      <ellipse cx="60" cy="62" rx="29" ry="35" fill={SKIN} />
      <path d="M30 60 Q28 24 60 26 Q92 24 90 60 Q82 40 60 40 Q38 40 30 60 Z" fill="#4a3427" />
      <path d="M46 34 Q58 30 72 36" stroke="#c9c4bd" strokeWidth="4" fill="none" strokeLinecap="round" />
      <circle cx="49" cy="64" r="11" fill="#fff" fillOpacity=".5" stroke="#2b2118" strokeWidth="2.4" />
      <circle cx="71" cy="64" r="11" fill="#fff" fillOpacity=".5" stroke="#2b2118" strokeWidth="2.4" />
      <path d="M60 64 h0" stroke="#2b2118" strokeWidth="2.4" />
      <circle cx="49" cy="65" r="2.2" fill={INK} />
      <circle cx="71" cy="65" r="2.2" fill={INK} />
      <path d="M42 51 q7 -4 14 0 M64 51 q7 -4 14 0" stroke="#4a3427" strokeWidth="2.4" fill="none" strokeLinecap="round" />
      <path d="M60 70 q-3 8 0 10" stroke="#c99974" strokeWidth="2" fill="none" strokeLinecap="round" />
      <path d="M50 88 q10 7 20 0" stroke="#a24b46" strokeWidth="3" fill="none" strokeLinecap="round" />
      <circle cx="31" cy="76" r="2.5" fill="#d9c27a" />
      <circle cx="89" cy="76" r="2.5" fill="#d9c27a" />
    </svg>
  );
}

// Ama: rounder face, glasses, short dark hair, red sweater.
function Ama() {
  return (
    <svg viewBox="0 0 120 150" role="img" aria-label="Accounting Ama, a round-faced man with glasses in a red sweater">
      <path d="M4 150 Q8 108 60 104 Q112 108 116 150 Z" fill="#b3322f" />
      <path d="M48 104 Q60 118 72 104" stroke="#8c2523" strokeWidth="5" fill="none" />
      <circle cx="60" cy="62" r="37" fill={SKIN} />
      <path d="M26 56 Q26 22 60 22 Q94 22 94 56 Q84 36 60 36 Q36 36 26 56 Z" fill="#2f2620" />
      <circle cx="40" cy="78" r="7" fill="#e9a08e" opacity=".55" />
      <circle cx="80" cy="78" r="7" fill="#e9a08e" opacity=".55" />
      <rect x="35" y="55" width="22" height="17" rx="5" fill="#fff" fillOpacity=".5" stroke="#2b2118" strokeWidth="2.4" />
      <rect x="63" y="55" width="22" height="17" rx="5" fill="#fff" fillOpacity=".5" stroke="#2b2118" strokeWidth="2.4" />
      <path d="M57 62 h6" stroke="#2b2118" strokeWidth="2.4" />
      <circle cx="46" cy="64" r="2.2" fill={INK} />
      <circle cx="74" cy="64" r="2.2" fill={INK} />
      <path d="M38 50 q8 -4 16 0 M66 50 q8 -4 16 0" stroke="#2f2620" strokeWidth="2.6" fill="none" strokeLinecap="round" />
      <path d="M60 70 q-3 7 1 9" stroke="#c99974" strokeWidth="2" fill="none" strokeLinecap="round" />
      <path d="M48 87 q12 8 24 0" stroke="#8a3a34" strokeWidth="3" fill="none" strokeLinecap="round" />
    </svg>
  );
}

// Father: grumpy, stubble, big nose, green flannel, and a coffee mug that steams only while he works.
function Father({ working }: Props) {
  return (
    <svg viewBox="0 0 120 150" role="img" aria-label="Facilities Father, a grumpy stubbly man in green with a coffee mug">
      <path d="M8 150 Q10 108 60 104 Q110 108 112 150 Z" fill="#3f6b45" />
      <path d="M22 130 H98 M22 142 H98 M40 108 V150 M80 108 V150" stroke="#2f5335" strokeWidth="2" opacity=".7" />
      <path d="M48 104 L60 120 L72 104" fill="#e8dfcf" />
      <path d="M31 50 Q32 24 60 24 Q88 24 89 50 Q80 36 60 36 Q40 36 31 50 Z" fill="#5a4a3c" />
      <ellipse cx="60" cy="62" rx="29" ry="35" fill="#e7bb93" />
      <path d="M33 74 Q36 98 60 100 Q84 98 87 74 Q80 88 60 88 Q40 88 33 74 Z" fill="#5a4a3c" opacity=".55" />
      <g fill="#5a4a3c" opacity=".7">
        {[40, 46, 52, 68, 74, 80, 44, 56, 64, 76].map((x, i) => (
          <circle key={i} cx={x} cy={80 + (i % 4) * 5} r="0.9" />
        ))}
      </g>
      <path d="M40 52 L56 58 M80 52 L64 58" stroke="#5a4a3c" strokeWidth="4" strokeLinecap="round" />
      <circle cx="49" cy="63" r="2.2" fill={INK} />
      <circle cx="71" cy="63" r="2.2" fill={INK} />
      <path d="M60 58 q-12 20 -4 24 q6 4 14 -1 q-4 -2 -3 -6 q2 -10 -7 -17 Z" fill="#d9a67c" />
      <path d="M46 91 q14 -8 28 0" stroke="#6b3d30" strokeWidth="3" fill="none" strokeLinecap="round" />
      {/* the coffee mug */}
      <g transform="translate(76 112)">
        <rect x="0" y="6" width="22" height="22" rx="4" fill="#f2ece1" stroke="#7b6a58" strokeWidth="1.5" />
        <path d="M22 11 q9 0 9 8 q0 7 -9 7" stroke="#7b6a58" strokeWidth="3" fill="none" />
        <rect x="2" y="8" width="18" height="5" fill="#5b3b24" />
        {working && (
          <g className="steam" stroke="#9a9185" strokeWidth="2" fill="none" strokeLinecap="round">
            <path className="s1" d="M6 4 q-4 -5 0 -9 q4 -4 0 -9" />
            <path className="s2" d="M12 4 q-4 -5 0 -9 q4 -4 0 -9" />
            <path className="s3" d="M18 4 q-4 -5 0 -9 q4 -4 0 -9" />
          </g>
        )}
      </g>
    </svg>
  );
}

// Jervis: formal butler, bald, handlebar moustache, grey waistcoat and bow tie.
function Jervis() {
  return (
    <svg viewBox="0 0 120 150" role="img" aria-label="Jervis, a bald butler with a moustache and a bow tie">
      <path d="M8 150 Q10 108 60 104 Q110 108 112 150 Z" fill="#6b6d72" />
      <path d="M46 106 L60 150 L74 106 Z" fill="#f6f2ea" />
      <path d="M52 124 L60 150 L68 124 Z" fill="#55575c" />
      <circle cx="60" cy="130" r="2" fill="#d9c27a" />
      <circle cx="60" cy="140" r="2" fill="#d9c27a" />
      <path d="M50 108 L60 114 L50 120 Z M70 108 L60 114 L70 120 Z" fill="#1d1d20" />
      <circle cx="60" cy="114" r="3" fill="#1d1d20" />
      <ellipse cx="60" cy="62" rx="28" ry="35" fill="#f0cdaa" />
      <path d="M32 66 q-4 -8 0 -16 M88 66 q4 -8 0 -16" stroke="#8d8a85" strokeWidth="5" fill="none" strokeLinecap="round" />
      <ellipse cx="50" cy="36" rx="10" ry="4" fill="#fff" opacity=".5" />
      <path d="M42 51 q7 -3 14 0 M64 48 q7 -5 14 0" stroke="#8d8a85" strokeWidth="2.6" fill="none" strokeLinecap="round" />
      <circle cx="49" cy="62" r="2.1" fill={INK} />
      <circle cx="71" cy="62" r="2.1" fill={INK} />
      <path d="M60 64 q-3 8 0 11" stroke="#c99974" strokeWidth="2" fill="none" strokeLinecap="round" />
      <path d="M60 80 q-8 -6 -18 -2 q-6 2 -6 8 q6 -4 12 -2 q8 2 12 -2 q4 4 12 2 q6 -2 12 2 q0 -6 -6 -8 q-10 -4 -18 2 Z" fill="#6b6865" />
      <path d="M52 92 q8 3 16 0" stroke="#8a5a50" strokeWidth="2.4" fill="none" strokeLinecap="round" />
    </svg>
  );
}

export function Avatar({ who, working }: { who: AgentKey; working?: boolean }) {
  switch (who) {
    case "boss":
      return <Boss />;
    case "ina":
      return <Ina />;
    case "ama":
      return <Ama />;
    case "father":
      return <Father working={working} />;
    case "jervis":
      return <Jervis />;
  }
}
