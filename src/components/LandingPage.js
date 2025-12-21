import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center justify-center p-4">
      <div className="max-w-4xl w-full bg-white rounded-2xl shadow-xl overflow-hidden">
        <div className="md:flex">
          <div className="md:flex-shrink-0 md:w-1/2 bg-gradient-to-r from-blue-600 to-indigo-700 flex items-center justify-center p-12">
            <div className="text-center">
              <h1 className="text-4xl font-extrabold text-white mb-4">AuthentiScan</h1>
              <div className="bg-white bg-opacity-20 rounded-full p-4 inline-block mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <p className="text-xl text-blue-100">AI Image Authenticity Detector</p>
            </div>
          </div>
          <div className="p-8 md:w-1/2">
            <div className="uppercase tracking-wide text-sm text-indigo-500 font-semibold">Combat Misinformation</div>
            <h2 className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              Distinguish Between AI-Generated and Real Images
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              In an era where artificial intelligence can create incredibly realistic images, it's becoming increasingly difficult to distinguish between what's real and what's generated. AuthentiScan uses advanced deep learning techniques to analyze images and determine their authenticity.
            </p>
            <p className="mt-4 text-lg text-gray-600">
              Our cutting-edge DenseNet-121 model, enhanced with transfer learning, provides highly accurate detection capabilities to help you verify the origin of any image.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row gap-4">
              <Link to="/signup" className="px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 transition duration-300 text-center">
                Get Started
              </Link>
              <Link to="/login" className="px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-indigo-700 bg-white hover:bg-gray-50 transition duration-300 text-center">
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </div>
      <div className="mt-8 text-center text-gray-600">
        <p>Powered by Deep Learning • Built with TensorFlow & React</p>
      </div>
    </div>
  );
};

export default LandingPage;