import Link from "next/link";
import { Instagram, Facebook, Mail, Phone } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-card border-t border-border mt-20">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <h3 className="text-2xl font-[family-name:var(--font-display)] text-primary">
              Lush Moments
            </h3>
            <p className="text-muted-foreground text-sm leading-relaxed">
              Creating unforgettable celebrations with elegant décor that brings
              your vision to life.
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h4 className="font-semibold text-foreground">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link
                  href="/"
                  className="text-muted-foreground hover:text-primary transition-colors"
                >
                  Home
                </Link>
              </li>
              <li>
                <Link
                  href="/gallery"
                  className="text-muted-foreground hover:text-primary transition-colors"
                >
                  Gallery
                </Link>
              </li>
              <li>
                <Link
                  href="/packages"
                  className="text-muted-foreground hover:text-primary transition-colors"
                >
                  Packages
                </Link>
              </li>
              <li>
                <Link
                  href="/booking"
                  className="text-muted-foreground hover:text-primary transition-colors"
                >
                  Book Now
                </Link>
              </li>
            </ul>
          </div>

          {/* Services */}
          <div className="space-y-4">
            <h4 className="font-semibold text-foreground">Services</h4>
            <ul className="space-y-2 text-sm">
              <li className="text-muted-foreground">Baby Showers</li>
              <li className="text-muted-foreground">Birthday Parties</li>
              <li className="text-muted-foreground">Engagements</li>
              <li className="text-muted-foreground">Custom Events</li>
            </ul>
          </div>

          {/* Contact */}
          <div className="space-y-4">
            <h4 className="font-semibold text-foreground">Get in Touch</h4>
            <ul className="space-y-3 text-sm">
              <li className="flex items-center gap-2 text-muted-foreground">
                <Phone className="h-4 w-4 text-primary" />
                <span>+251 951 06 70 43</span>
              </li>
              <li className="flex items-center gap-2 text-muted-foreground">
                <Mail className="h-4 w-4 text-primary" />
                <span>hello@lushmoments.com</span>
              </li>
            </ul>
            <div className="flex gap-4 pt-2">
              <a
                href="https://instagram.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-primary transition-colors"
                aria-label="Instagram"
              >
                <Instagram className="h-5 w-5" />
              </a>
              <a
                href="https://facebook.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-primary transition-colors"
                aria-label="Facebook"
              >
                <Facebook className="h-5 w-5" />
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-border mt-8 pt-8 text-center text-sm text-muted-foreground">
          <p>
            &copy; {new Date().getFullYear()} Lush Moments. All rights reserved.
          </p>
          <p>
            Designed and Developed by{" "}
            <a href="https://nahom.codes" className="border-b-2 border-b-white">
              Nahom_d54
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
}
