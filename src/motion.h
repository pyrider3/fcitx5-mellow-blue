// SPDX-License-Identifier: LGPL-2.1-or-later
#pragma once
#include <algorithm>
#include <cmath>
#include <cstdint>
namespace smoothui {
struct Box {
    double x=0,y=0,w=0,h=0;
    bool operator==(const Box &b) const {
        return std::abs(x-b.x)<.001 && std::abs(y-b.y)<.001 && std::abs(w-b.w)<.001 && std::abs(h-b.h)<.001;
    }
};
// 80 ms cubic ease-out. Retarget from the currently displayed position.
class Motion {
public:
    static constexpr uint64_t duration=80000;
    Box start{},target{};
    uint64_t began=0;
    bool initialized=false,running=false;
    void reset() { initialized=false;running=false; }
    Box sample(uint64_t now) const {
        if(!running) return target;
        double t=std::clamp(double(now>=began?now-began:0)/duration,0.0,1.0);
        double k=1-std::pow(1-t,3);
        return {start.x+(target.x-start.x)*k,start.y+(target.y-start.y)*k,
                start.w+(target.w-start.w)*k,start.h+(target.h-start.h)*k};
    }
    void set(Box next,uint64_t now,bool snap) {
        if(snap || !initialized) {start=target=next;began=now;initialized=true;running=false;return;}
        if(next==target) return;
        start=sample(now);target=next;began=now;running=!(start==target);
    }
    bool active(uint64_t now) {
        if(running && now>=began && now-began>=duration) running=false;
        return running;
    }
};
}

namespace smoothui {
// The engine's visibility is independent from this visual transition.
class PopupFade {
public:
    enum class Phase { Hidden, Opening, Shown, Closing };
    Phase phase=Phase::Hidden;
    double from=0,to=0,fromOffset=0;
    uint64_t began=0,duration=0;
    double opacity(uint64_t now) const {
        if(phase==Phase::Hidden) return 0;
        if(phase==Phase::Shown) return 1;
        double t=std::clamp(double(now>=began?now-began:0)/duration,0.0,1.0);
        double k=1-std::pow(1-t,3);
        return from+(to-from)*k;
    }
    double offset(uint64_t now) const {
        if(phase==Phase::Closing) return fromOffset;
        if(phase!=Phase::Opening) return 0;
        double t=std::clamp(double(now>=began?now-began:0)/duration,0.0,1.0);
        return fromOffset*std::pow(1-t,3);
    }
    void open(uint64_t now) {
        if(phase==Phase::Opening || phase==Phase::Shown) return;
        fromOffset=phase==Phase::Hidden?2:offset(now);
        from=opacity(now);to=1;began=now;duration=90000;phase=Phase::Opening;
    }
    void close(uint64_t now) {
        if(phase==Phase::Closing || phase==Phase::Hidden) return;
        fromOffset=offset(now);
        from=opacity(now);to=0;began=now;duration=60000;phase=Phase::Closing;
    }
    bool step(uint64_t now) {
        if((phase==Phase::Opening || phase==Phase::Closing) && now>=began && now-began>=duration) {
            phase=to==1?Phase::Shown:Phase::Hidden;
        }
        return phase==Phase::Opening || phase==Phase::Closing;
    }
    bool closing() const { return phase==Phase::Closing; }
    void reset() {phase=Phase::Hidden;from=to=fromOffset=0;}
};
}
