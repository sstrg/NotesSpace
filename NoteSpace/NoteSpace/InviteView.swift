//
//  InviteView.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import SwiftUI
import CoreImage.CIFilterBuiltins

struct InviteView: View {
    let space: Space
    @Environment(\.dismiss) var dismiss
    @State private var inviteLink = ""
    @State private var qrCodeImage: Image?
    
    let context = CIContext()
    let filter = CIFilter.qrCodeGenerator()
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 30) {
                    // Название пространства
                    VStack(spacing: 8) {
                        Text(space.name)
                            .font(.title2)
                            .fontWeight(.bold)
                        
                        Text("Join to space")
                            .font(.subheadline)
                            .foregroundColor(.gray)
                    }
                    .padding(.top)
                    
                    // QR-код
                    VStack(spacing: 15) {
                        if let qrCodeImage = qrCodeImage {
                            qrCodeImage
                                .interpolation(.none)
                                .resizable()
                                .scaledToFit()
                                .frame(width: 250, height: 250)
                                .padding()
                                .background(Color.white)
                                .cornerRadius(20)
                                .shadow(radius: 5)
                        } else {
                            ProgressView()
                                .frame(width: 250, height: 250)
                        }
                        
                        Text("Scan QR with iPhone camera")
                            .font(.caption)
                            .foregroundColor(.blue)
                            .padding(.horizontal)
                            .multilineTextAlignment(.center)
                    }
                    
                    // Код приглашения
                    VStack(spacing: 10) {
                        Text("Or use code:")
                            .font(.headline)
                        
                        HStack {
                            Spacer()
                            Text(space.inviteCode)
                                .font(.system(size: 32, weight: .bold, design: .monospaced))
                                .padding()
                                .background(Color.gray.opacity(0.1))
                                .cornerRadius(10)
                            
                            Button(action: copyInviteCode) {
                                Image(systemName: "doc.on.doc")
                                    .font(.title2)
                                    .foregroundColor(.blue)
                                    .padding(.leading, 5)
                            }
                            Spacer()
                        }
                    }
                    
                    // Информация о пространстве
                    VStack(spacing: 8) {
                        HStack {
                            Image(systemName: "person.2")
                            Text("\(space.memberIds.count) участников")
                            Spacer()
                        }
                        .foregroundColor(.gray)
                        .padding(.horizontal)
                        
                        if space.memberIds.count > 1 {
                            HStack {
                                Image(systemName: "clock")
                                Text("Join!")
                                Spacer()
                            }
                            .foregroundColor(.gray)
                            .padding(.horizontal)
                        }
                    }
                    .padding(.top)
                    
                    Spacer()
                }
                .padding()
            }
            .navigationTitle("Add")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Close") {
                        dismiss()
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: shareInvite) {
                        Image(systemName: "square.and.arrow.up")
                    }
                }
            }
            .onAppear {
                inviteLink = DataManager.shared.getSpaceInviteLink(spaceId: space.id)
                generateQRCode(from: space.inviteCode)
            }
        }
    }
    
    private func generateQRCode(from string: String) {
        filter.message = Data(string.utf8)
        
        if let outputImage = filter.outputImage {
            if let cgimg = context.createCGImage(outputImage, from: outputImage.extent) {
                let uiImage = UIImage(cgImage: cgimg)
                qrCodeImage = Image(uiImage: uiImage)
            }
        }
    }
    
    private func copyInviteCode() {
        UIPasteboard.general.string = space.inviteCode
        
        // Простая обратная связь
        let generator = UINotificationFeedbackGenerator()
        generator.notificationOccurred(.success)
    }
    
    private func shareInvite() {
        let text = "Join to my space '\(space.name)' in NoteSpace! Use code: \(space.inviteCode)"
        let av = UIActivityViewController(activityItems: [text], applicationActivities: nil)
        
        if let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
           let rootViewController = windowScene.windows.first?.rootViewController {
            rootViewController.present(av, animated: true)
        }
    }
}
