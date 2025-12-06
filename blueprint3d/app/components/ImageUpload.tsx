"use client";

import { ChangeEvent, useState, DragEvent } from "react";
import Image from "next/image";

interface ImageUploadProps {
    onImageSelect: (file: File) => void;
    selectedImage: File | null;
}

export default function ImageUpload({ onImageSelect, selectedImage }: ImageUploadProps) {
    const [dragActive, setDragActive] = useState(false);
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);

    const handleFile = (file: File) => {
        if (file && (file.type.startsWith("image/") || file.type === "application/pdf")) {
            onImageSelect(file);
            const url = URL.createObjectURL(file);
            setPreviewUrl(url);
        }
    };

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleDrag = (e: DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e: DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    return (
        <div className="form-group">
            <label className="label">1. 上传工程图纸</label>
            <div
                className={`upload-area ${dragActive ? 'active' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => document.getElementById('file-upload')?.click()}
            >
                <input
                    id="file-upload"
                    type="file"
                    className="hidden"
                    accept="image/*,application/pdf"
                    onChange={handleChange}
                    style={{ display: 'none' }}
                />

                {previewUrl ? (
                    <div style={{ width: '100%', height: '100%' }}>
                        <img
                            src={previewUrl}
                            alt="Preview"
                            className="preview-thumbnail"
                        />
                        <p className="text-sm text-gray-500">{selectedImage?.name}</p>
                        <p className="text-xs text-primary mt-2">点击或拖拽替换</p>
                    </div>
                ) : (
                    <div className="flex flex-col items-center gap-2">
                        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-gray-400">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                            <polyline points="17 8 12 3 7 8" />
                            <line x1="12" y1="3" x2="12" y2="15" />
                        </svg>
                        <p>点击或拖拽上传图片</p>
                        <p className="text-xs text-secondary">支持 JPG, PNG, PDF</p>
                    </div>
                )}
            </div>
        </div>
    );
}
